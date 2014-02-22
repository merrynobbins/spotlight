import xbmcgui

class ListItemFactory:
    
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
    
   
