import xbmc

class TrackList:
    
    def __init__(self, converter):
        self.converter = converter
        self.xbmc_player = xbmc.Player()
        self.xbmc_playlist = xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
        
    def set_track_uris(self, uris):
        self.track_uris = uris
        self.tracks = map(lambda uri : self.converter.uri_to_track(uri), uris)
           
    def set_starting_track_uri(self, uri):
        self.starting_track_uri = uri
        self.starting_track = self.converter.uri_to_track(uri)
        
    def play(self):
        self.xbmc_playlist.clear()
        for track in self.tracks:
            path, listitem = self.converter.track_to_list_item(track)
            self.xbmc_playlist.add(path, listitem)
        self.xbmc_player.playselected(self.calculate_offset())

    def calculate_offset(self):
        if self.starting_track is None:
            return 0
                
        return self.track_uris.index(self.starting_track_uri)

            
                
   