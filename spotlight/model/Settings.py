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

import xbmcaddon

class Settings:
    
    ADD_ON_ID = 'plugin.audio.spotlight'
    
    LABEL_TO_BITRATE = {
                        '96kbps' : 2,
                        '160kbps' :0,
                        '320bps' : 1,
                        }
    
    def __init__(self):
        self.addon = xbmcaddon.Addon(Settings.ADD_ON_ID)
        
    @property        
    def username(self):
        
        return self.addon.getSetting('username')
    
    @property
    def password(self):
        
        return self.addon.getSetting('password')
    
    @property
    def max_cache_size(self):
        
        return int(self.addon.getSetting('max_cache_size'))
    
    @property
    def preferred_bitrate(self):
        bitrate_label = self.addon.getSetting('preferred_bitrate')
        
        return Settings.LABEL_TO_BITRATE.get(bitrate_label)
    
    @property
    def volume_normalization(self):
        
        return self.addon.getSetting('value_normalization')
    
    @property
    def internal_server_port(self):
        
        return int(self.addon.getSetting('internal_server_port'))