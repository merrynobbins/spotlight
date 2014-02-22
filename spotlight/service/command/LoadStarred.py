from spotlight.service.util.SynchronizerMixin import SynchronizerMixin
from spotify.playlist import PlaylistCallbacks

class LoadStarred(SynchronizerMixin, PlaylistCallbacks):
    
    def __init__(self, session):
        self.session = session
    
    def before_wait(self):
        self.playlist.add_callbacks(self)        
    
    def execute(self):
        self.playlist = self.session.starred_create()
        
        if self.playlist.is_loaded():
            self.disable_wait()
        
        return self.playlist
    
    def playlist_state_changed(self, playlist):
        if playlist.is_loaded(): 
            self.done()
            
    def clean_up(self):
        self.playlist.remove_callbacks(self)