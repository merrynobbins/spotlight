from spotilight.service.util.SynchronizerMixin import SynchronizerMixin
from spotify.artistbrowse import Artistbrowse, ArtistbrowseCallbacks, BrowseType

class BrowseArtist(SynchronizerMixin, ArtistbrowseCallbacks):
    
    def __init__(self, artist, session):
        self.artist = artist
        self.session = session
    
    def execute(self):
        
        return Artistbrowse(self.session, self.artist, BrowseType.Full, self)
    
    def artistbrowse_complete(self, artistbrowse):
        self.done()
