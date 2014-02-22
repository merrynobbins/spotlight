from spotify.session import SessionCallbacks
from spotify import ErrorType
import xbmc

class SpotifyCallbacks(SessionCallbacks):
    
    def __init__(self, main_loop, audio_buffer, authenticator):
        self.main_loop = main_loop
        self.audio_buffer = audio_buffer
        self.authenticator = authenticator
    
    def logged_in(self, session, error):
        
        xbmc.log("libspotify: logged in: %d" % error)
        
        if error != ErrorType.Ok:                        
            self.authenticator.error()
        else:
            self.authenticator.logged_in()
        
    def logged_out(self, session):
        xbmc.log('Spotify logged out.')
        
    def connection_error(self, session, error):
        xbmc.log("libspotify: conn error: %d" % error)
        self.authenticator.error()
        
    def connectionstate_updated(self, session):
        self.authenticator.logged_in()
        
    def message_to_user(self, session, data):
        xbmc.log("libspotify: msg: %s" % data)
    
    def log_message(self, session, data):
        xbmc.log("libspotify log: %s" % data)
    
    def streaming_error(self, session, error):
        xbmc.log("libspotify: streaming error: %d" % error)
        self.authenticator.error()
        
    def metadata_updated(self, session):
        xbmc.log("libspotify: metadata updated")
        
    def notify_main_thread(self, session):
        xbmc.log("libspotify: notified main thread")
        self.main_loop.notify()
        
    def music_delivery(self, session, data, num_samples, sample_type, sample_rate, num_channels):
        xbmc.log("libspotify: music delivery samples = %d" % num_samples)
        return self.audio_buffer.music_delivery(data, num_samples, sample_type, sample_rate, num_channels)