# 
#  Copyright © Dariusz Biskup
#  
#  This file is part of Spotlight
# 
#  Spotlight is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as 
#  published by the Free Software Foundation; either version 3 of 
#  the License, or (at your option) any later version.
#  
#  Spotlight is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>
#  

from spotlight.service.util.SessionGuard import SessionGuard
from spotlight.service.command.LoadTrack import LoadTrack
from spotlight.service.command.LoadStarred import LoadStarred
from spotlight.service.command.LoadAlbum import LoadAlbum
from spotlight.service.command.BrowseAlbum import BrowseAlbum
from spotlight.service.command.BrowseArtist import BrowseArtist
from spotlight.service.util.AlbumFilter import AlbumFilter
from spotlight.service.command.Search import Search

class LocalService:
    
    def __init__(self, session, authenticator, model_factory):
        self.session = session
        self.model_factory = model_factory
        self.authenticator = authenticator

    @SessionGuard
    def search(self, query):
        search_result = Search(query, self.session).run_and_wait()
        tracks = LoadTrack.from_list(search_result.tracks(), self.session)
    
        return self.model_factory.to_track_list_model(tracks)
    
    @SessionGuard
    def starred(self):
        search_result = LoadStarred(self.session).run_and_wait()
        tracks = LoadTrack.from_list(search_result.tracks(), self.session)
         
        return self.model_factory.to_track_list_model(tracks)

    @SessionGuard
    def playlists(self):
        container = self.session.playlistcontainer()

        return self.model_factory.to_playlist_list_model(container.playlists())
    
    @SessionGuard
    def playlist_tracks(self, name):
        container = self.session.playlistcontainer()
        matched_playlists = filter(lambda playlist : playlist.name() == name, container.playlists())
        if (len(matched_playlists) > 0):
            playlist = matched_playlists[0]
            tracks = LoadTrack.from_list(playlist.tracks(), self.session)
            return self.model_factory.to_track_list_model(tracks)
        
        return []    
    
    @SessionGuard
    def album_tracks(self, album_uri):
        album = LoadAlbum.from_uri(album_uri, self.session)
        browse = BrowseAlbum(album, self.session).run_and_wait()
        tracks = LoadTrack.from_list(browse.tracks(), self.session)
    
        return self.model_factory.to_track_list_model(tracks)
    
    @SessionGuard
    def artist_albums(self, track_uri):
        track = LoadTrack.from_uri(track_uri, self.session)
        browse = BrowseArtist(track.album().artist(), self.session).run_and_wait()
        albums = AlbumFilter(browse.albums()).filter()
    
        return self.model_factory.to_album_list_model(albums)
       
    