from spotilight.service.session.SpotifyCallbacks import SpotifyCallbacks
from spotilight.service.session.MainLoopThread import MainLoopThread
from spotilight.service.session.appkey import appkey
from spotilight.service.util.Settings import Settings
from spotify.session import Session
from spotify import MainLoop, Bitrate
import os
import xbmc
from spotilight.service.session.Authenticator import Authenticator

class SpotifySetup:
    
    def __init__(self, audio_buffer, authenticator):
        self.settings = Settings()       
        self.audio_buffer = audio_buffer
        self.authenticator = authenticator
    
    def launch(self):
        data_dir, cache_dir, settings_dir = self.check_dirs()        
        main_loop = MainLoop()
        callbacks = SpotifyCallbacks(main_loop, self.audio_buffer, self.authenticator)
        self.session = Session(
            callbacks,
            app_key=appkey,
            user_agent="python ctypes bindings",
            settings_location=settings_dir,
            cache_location=cache_dir,
            dont_save_metadata_for_playlists=True,
            initially_unload_playlists=False,
        )
        self.authenticator.set_session(self.session)
        self.set_settings(self.session);
        runner = MainLoopThread(main_loop, self.session)
        runner.start()        
         
        return self.session
        
    def set_settings(self, session):
        session.set_cache_size(500)
        session.preferred_bitrate(Bitrate.Rate160k)
        session.set_volume_normalization(False)   
            
     
    def check_dirs(self):
        addon_data_dir = os.path.join(
            xbmc.translatePath('special://profile/addon_data'),
            'plugin.audio.spotifyxbmcplugin'
        )
        
        # Auto-create profile dir if it does not exist
        if not os.path.exists(addon_data_dir):
            os.makedirs(addon_data_dir)
        
        # Libspotify cache & settings
        sp_cache_dir = os.path.join(addon_data_dir, 'libspotify/cache')
        sp_settings_dir = os.path.join(addon_data_dir, 'libspotify/settings')
        
        if not os.path.exists(sp_cache_dir):
            os.makedirs(sp_cache_dir)
        
        if not os.path.exists(sp_settings_dir):
            os.makedirs(sp_settings_dir)
        
        return (addon_data_dir, sp_cache_dir, sp_settings_dir)  
