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
    
        
    