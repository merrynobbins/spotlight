# 
#  Copyright (c) Dariusz Biskup
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

from spotlight.model.Model import Model
from spotify import image, link, playlist
from spotify.playlist import Playlist
from spotify.link import LinkType

class ModelFactory:
    
    def __init__(self, url_gen):
        self.url_gen = url_gen
    
    def to_album_model(self, album):
        
        return Model(
                name=album.name(),
                year=album.year(),
                image=self.url_gen.get_image_url(album.cover(image.ImageSize.Large)),
                uri=self.url_gen.get_album_uri(album))
    
    def to_track_model(self, track):
                    
        return Model(track=track.name(),
                     album=track.album().name(),
                     artist=track.album().artist().name(),
                     uri=link.create_from_track(track).as_string(),
                     type=link.create_from_track(track).type(),
                     album_uri=self.url_gen.get_album_uri(track.album()),
                     iconImage=self.url_gen.get_icon_url(track),
                     thumbnailImage=self.url_gen.get_thumbnail_url(track),
                     path=self.url_gen.get_track_url(track),
                     time=track.duration() / 1000)

    def to_playlist_list_model(self, playlists):

        return [self.to_playlist_model(playlist, index) for index, playlist in enumerate(playlists)]
   
    def to_playlist_model(self, playlist, index):
        playlist_link = link.create_from_playlist(playlist)
        uri = ''
        if playlist_link is not None:
            uri = playlist_link.as_string()
            
        return Model(name = playlist.name(), user = playlist.owner().canonical_name(), index = index, uri = uri)
    
    def to_artist_model(self, artist):
        
        return Model(name = artist.name(), uri = link.create_from_artist(artist).as_string())
    
    def to_track_list_model(self, tracks):
    
        return map(lambda track:self.to_track_model(track), tracks)
    
    def to_album_list_model(self, albums):
    
        return map(lambda album:self.to_album_model(album), albums)
    
    def to_artist_list_model(self, artists):
    
        return map(lambda artist:self.to_artist_model(artist), artists)
    
    def to_inbox_model(self, items, session):
        track_links = [link.create_from_track(track) for track in items]
        
        albums = [track_link.as_album() 
                  for track_link in track_links if track_link.type() is LinkType.Album]
        artists = [track_link.as_artist() 
                   for track_link in track_links if track_link.type() is LinkType.Artist]
        tracks = [track_link.as_track() 
                  for track_link in track_links if track_link.type() is LinkType.Track]
        playlists = [Playlist(playlist.create(session, track_link)) 
                     for track_link in track_links if track_link.type() is LinkType.Playlist]
        
        return Model(albums = self.to_album_list_model(albums),
                     artists = self.to_artist_list_model(artists),
                     tracks = self.to_track_list_model(tracks),
                     playlists = self.to_playlist_list_model(playlists))
    
    def clean_up(self):
        self.url_gen.clean_up()
        