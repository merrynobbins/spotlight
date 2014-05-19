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

import xbmcgui

class ListItemFactory:
    
    def create_list_item(self, track_model, index = 0):
        path = track_model.path
        item = xbmcgui.ListItem('%s - %s' % (track_model.artist, track_model.track),
                      iconImage = track_model.iconImage,
                      thumbnailImage = track_model.thumbnailImage, 
                      path = track_model.path)        
        item.setInfo('music', {'album':track_model.album, 
                     'artist':track_model.artist, 
                     'title' : track_model.track,            
                     'duration':track_model.time, 
                     'tracknumber' : index})
        
        return path, item
    
   
