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

from threading import Event
import xbmc
from spotify import ConnectionState

class Authenticator:
    
    WAIT_TIMEOUT = 10
    
    def set_session(self, session):
        self.session = session
        self.flag = Event()
    
    def login(self, username, password):      
        xbmc.log('Logging in')  
        self.session.login(username, password)
        self.flag.wait(Authenticator.WAIT_TIMEOUT)
        xbmc.log('Lock released')        
        return self.connection_state()
        
    def connection_state(self):
        return self.session.connectionstate()
        
    def logged_in(self):
        xbmc.log('Got logged in callback')
        self.release_lock_if_logged()
        
    def error(self):
        xbmc.log('Got error callback')
        self.release_lock()
        
    def release_lock_if_logged(self):
        if self.connection_state() == ConnectionState.LoggedIn:
            self.release_lock()
            
    def release_lock(self):
        self.flag.set()
        self.flag.clear()