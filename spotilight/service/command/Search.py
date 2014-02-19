from spotilight.service.util.SynchronizerMixin import SynchronizerMixin
from spotify import search
from spotify.search import SearchCallbacks

class Search(SynchronizerMixin, SearchCallbacks):
    
    def __init__(self, query, session):
        self.query = query
        self.session = session
    
    def execute(self):
        self.search_result = search.Search(
            self.session, self.query,
            track_offset = 0, track_count = 100,
            callbacks = self)
        
        return self.search_result
    
    def search_complete(self, result):
        self.done(result)
