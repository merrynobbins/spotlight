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
from spotify import image, link

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
                     album_uri=self.url_gen.get_album_uri(track.album()),
                     iconImage=self.url_gen.get_icon_url(track),
                     thumbnailImage=self.url_gen.get_thumbnail_url(track),
                     path=self.url_gen.get_track_url(track),
                     time=track.duration() / 1000)

    def to_playlist_list_model(self, playlists):

        return [self.to_playlist_model(playlist, index) for index, playlist in enumerate(playlists)]
   
    def to_playlist_model(self, playlist, index):
        
        return Model(name = playlist.name(), index = index)
    
    def to_track_list_model(self, tracks):
    
        return map(lambda track:self.to_track_model(track), tracks)
    
    def to_album_list_model(self, albums):
    
        return map(lambda album:self.to_album_model(album), albums)
    
    def clean_up(self):
        self.url_gen.clean_up()
    