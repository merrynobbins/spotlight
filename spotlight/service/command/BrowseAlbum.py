from spotlight.service.util.SynchronizerMixin import SynchronizerMixin
from spotify.albumbrowse import AlbumbrowseCallbacks, Albumbrowse

class BrowseAlbum(SynchronizerMixin, AlbumbrowseCallbacks):
    
    def __init__(self, album, session):
        self.album = album
        self.session = session
    
    def execute(self):

        return Albumbrowse(self.session, self.album, self)
    
    def albumbrowse_complete(self, albumbrowse):
        self.done()
