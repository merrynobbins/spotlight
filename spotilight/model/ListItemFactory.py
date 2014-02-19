import xbmcgui

class ListItemFactory:
    
#     def __init__(self, session, proxy_info):
#         self.session = session
#         self.host = proxy_info.host
#         self.port = proxy_info.port
#         self.proxy_info = proxy_info 
#     
#     def uri_to_list_item(self, uri):
#         track = self.uri_to_track(uri)
#         path, item = self.track_to_list_item(track)
#         return path, item
# 
#     def uri_to_track(self, uri):
#         track_link = link.create_from_string(uri)
#         track = track_link.as_track()
#         return track
    
    def create_list_item(self, track_model, index = 0):
        path = track_model.path
        item = xbmcgui.ListItem('%s - %s' % (track_model.album, track_model.track), 
                      iconImage = track_model.iconImage,
                      thumbnailImage = track_model.thumbnailImage, 
                      path = track_model.path)        
        item.setInfo('music', {'album':track_model.album, 
                     'artist':track_model.artist, 
                     'title' : track_model.track,            
                     'duration':track_model.time, 
                     'tracknumber' : index})
        
        return path, item
    
   
