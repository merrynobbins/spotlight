from spotify import link
from spotify.session import SessionCallbacks

from spotilight.service.util.SynchronizerMixin import SynchronizerMixin


class LoadTrack(SynchronizerMixin, SessionCallbacks):
    
    def __init__(self, track, session):
        self.track = track
        self.session = session
        
    def before_wait(self):
        self.session.add_callbacks(self)
    
    def execute(self):
        if self.track.is_loaded():
            self.disable_wait()
         
        return self.track
    
    def metadata_updated(self, session):
        if self.track.is_loaded():
            self.done(None)
            
    def clean_up(self):
        self.session.remove_callbacks(self)
        
    @staticmethod        
    def from_uri(uri, session):
        track_link = link.create_from_string(uri)
        track = track_link.as_track()
        return LoadTrack(track, session).run_and_wait()

    @staticmethod
    def from_list(tracks, session):
        return filter(lambda track : track.is_loaded(), 
                      map(lambda track : LoadTrack(track, session).run_and_wait(), tracks))
