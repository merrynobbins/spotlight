from spotilight.service.playback.TrackList import TrackList

class Player:
    
    def __init__(self, session, converter):        
        self.track_list = TrackList(converter)

    def play(self, track):
        self.track_list.set_track_uris([track.uri])
        self.track_list.play()

    def play_list(self, track_uris, starting_track_uri):
        self.track_list.set_track_uris(track_uris)
        self.track_list.set_starting_track_uri(starting_track_uri)        
        self.track_list.play()


    