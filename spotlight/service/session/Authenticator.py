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