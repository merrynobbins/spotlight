from spotify import link
from spotify.session import SessionCallbacks

from spotilight.service.util.SynchronizerMixin import SynchronizerMixin


class LoadAlbum(SynchronizerMixin, SessionCallbacks):
    
    def __init__(self, album, session):
        self.album = album
        self.session = session
        
    def before_wait(self):
        self.session.add_callbacks(self)
    
    def execute(self):
        if self.album.is_loaded():
            self.disable_wait()
         
        return self.album
    
    def metadata_updated(self, session):
        if self.album.is_loaded():
            self.done(None)
            
    def clean_up(self):
        self.session.remove_callbacks(self)
        
    @staticmethod        
    def from_uri(uri, session):
        album_link = link.create_from_string(uri)
        album = album_link.as_album()
        return album
