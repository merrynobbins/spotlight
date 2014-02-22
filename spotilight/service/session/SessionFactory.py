from spotilight.service.session.appkey import appkey
from spotify.session import Session
import os
import xbmc

class SessionFactory:
    
    def __init__(self, callbacks, settings):
        self.settings = settings       
        self.callbacks = callbacks
    
    def create_session(self):
        cache_dir = self.addon_dir('libspotify/cache')        
        settings_dir = self.addon_dir('libspotify/settings')        
        
        self.session = Session(
            self.callbacks,
            app_key=appkey,
            user_agent="spotlight",
            settings_location=settings_dir,
            cache_location=cache_dir,
            dont_save_metadata_for_playlists=True,
            initially_unload_playlists=False,
        )
        self.set_settings(self.session);
         
        return self.session
        
    def set_settings(self, session):
        session.set_cache_size(self.settings.max_cache_size)
        session.preferred_bitrate(self.settings.preferred_bitrate)
        session.set_volume_normalization(self.settings.volume_normalization)   
            
    def addon_dir(self, local_dir):
        data_dir = xbmc.translatePath('special://profile/addon_data')
        addon_data_dir = os.path.join(data_dir, 'plugin.audio.spotlight')
        
        return self.create_if_not_exist(os.path.join(addon_data_dir, local_dir))        
    
    def create_if_not_exist(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        return directory
            
