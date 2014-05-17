from spotify.playlistcontainer import PlaylistContainerCallbacks

class PlaylistCallbacks(PlaylistContainerCallbacks):
    
    def __init__(self, cache_storage):
        self.cache_storage = cache_storage
    
    def playlist_added(self, container, playlist, position):
        pass
        
    def playlist_removed(self, container, playlist, position):
        pass
    
    def playlist_moved(self, container, playlist, position, new_position):
        pass
    
    def container_loaded(self, container):
        pass
    