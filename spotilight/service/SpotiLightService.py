from spotilight.service.util.SessionGuard import SessionGuard
from spotilight.service.command.Search import Search
from spotilight.service.command.LoadStarred import LoadStarred
from spotilight.service.command.BrowseAlbum import BrowseAlbum
from spotilight.service.command.BrowseArtist import BrowseArtist
from spotilight.service.command.LoadTrack import LoadTrack
from spotilight.service.command.LoadAlbum import LoadAlbum
from spotilight.service.util.AlbumFilter import AlbumFilter
from spotilight.model.Model import Model

class SpotiLightService:
    
    def __init__(self, session, player, authenticator, converter):
        self.session = session
        self.player = player
        self.converter = converter
        self.authenticator = authenticator

    @SessionGuard
    def search(self, query):
        search_result = Search(query, self.session).run_and_wait()
        tracks = LoadTrack.from_list(search_result.tracks(), self.session)
    
        return self.from_spotify_tracks(tracks)
    
    @SessionGuard
    def starred(self):
        search_result = LoadStarred(self.session).run_and_wait()
        tracks = LoadTrack.from_list(search_result.tracks(), self.session)
         
        return self.from_spotify_tracks(tracks)

    @SessionGuard
    def playlists(self):
        container = self.session.playlistcontainer()

        return self.from_playlists(container.playlists())

    @SessionGuard
    def play(self, track_obj):
        self.player.play(Model(**track_obj))

        return {}
    
    @SessionGuard
    def play_list(self, track_uris, starting_track_uri):
        self.player.play_list(track_uris, starting_track_uri)
        
        return {}
    
    @SessionGuard
    def playlist_tracks(self, name):
        container = self.session.playlistcontainer()
        matched_playlists = filter(lambda playlist : playlist.name() == name, container.playlists())
        if (len(matched_playlists) > 0):
            playlist = matched_playlists[0]
            tracks = LoadTrack.from_list(playlist.tracks(), self.session)
            return self.from_spotify_tracks(tracks)
        
        return []    
    
    @SessionGuard
    def album_tracks(self, album_uri):
        album = LoadAlbum.from_uri(album_uri, self.session)
        browse = BrowseAlbum(album, self.session).run_and_wait()
        tracks = LoadTrack.from_list(browse.tracks(), self.session)
    
        return self.from_spotify_tracks(tracks)
    
    @SessionGuard
    def artist_albums(self, track_uri):
        track = LoadTrack.from_uri(track_uri, self.session)
        browse = BrowseArtist(track.album().artist(), self.session).run_and_wait()
        albums = AlbumFilter(browse.albums()).filter()
    
        return self.from_spotify_albums(albums)
    
    def from_playlists(self, playlists):

        return [self.from_playlist(playlist, index) for index, playlist in enumerate(playlists)]
   
    def from_playlist(self, playlist, index):
        
        return Model(name = playlist.name(), index = index)
    
    def from_spotify_tracks(self, tracks):
    
        return map(lambda track:self.from_spotify(track), tracks)
    
    def from_spotify_albums(self, albums):
    
        return map(lambda album:self.from_spotify_album(album), albums)
    
    def from_spotify_album(self, album):
        
        return self.converter.to_album_message(album)
    
    def from_spotify(self, spotify_track):
                    
        return self.converter.to_track_message(spotify_track)
    