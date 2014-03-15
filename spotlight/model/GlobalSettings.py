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

import xbmcaddon

class GlobalSettings:
    
    ADD_ON_ID = 'plugin.audio.spotlight'
    
    def __init__(self):
        self.addon = xbmcaddon.Addon(GlobalSettings.ADD_ON_ID)
    
    @property
    def internal_server_port(self):
        
        return int(self.addon.getSetting('internal_server_port'))