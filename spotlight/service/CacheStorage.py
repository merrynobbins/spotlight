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
from spotify.utils.decorators import synchronized

class Cache:
    
    def __init__(self, name):
        self.name = name
        self.invalidate()
        
    def invalidate(self):
        self.map = {}
        
    def update(self, key, value):
        self.map[key] = value
        
    def get(self, key):
        return self.map.get(key)
        
        
class CacheStorage:
    
    caches = {}
        
    def get_cache(self, key):
        cache = self.caches.get(key)
        if cache is None:
            cache = Cache(key)
            self.caches[key] = cache
        return cache
                 
    def invalidate(self, key):
        cache = self.caches.get(key)
        if cache is not None:
            cache.invalidate()
          
    def invalidate_all(self):
        for key, value in self.caches.iteritems() :
            value.invalidate()
            
            
        
        
    