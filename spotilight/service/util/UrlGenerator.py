from spotify import image, link

class UrlGenerator:
    
    def __init__(self, session, proxy_info):
        self.session = session
        self.host = proxy_info.host
        self.port = proxy_info.port
        self.proxy_info = proxy_info
    
    def get_icon_url(self, track):
        ready_track = self.get_playable_if_local(track)
        
        return self.get_image_url(ready_track.album().cover(image.ImageSize.Large))

    def get_thumbnail_url(self, track):
        ready_track = self.get_playable_if_local(track)
        
        return self.get_image_url(ready_track.album().cover())
        
    def get_playable_if_local(self, track):
        if track.is_local(self.session):
            return track.get_playable(self.session)

        return track
    
    def get_track_url(self, track):
        track_id = self.get_track_id(track)
        headers = self.proxy_info.url_headers
        
        return 'http://%s:%s/track/%s.wav|%s' % (self.host, self.port, track_id, headers)
    
    def get_image_url(self, image_id):

        return 'http://%s:%s/image/%s.jpg' % (self.host, self.port, image_id)
    
    def get_track_id(self, track):

        return link.create_from_track(track).as_string()[14:]
    
    def get_album_uri(self, album):

        return link.create_from_album(album).as_string()
    
