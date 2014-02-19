import types
from spotify import ConnectionState
from spotilight.service.util.Settings import Settings
import xbmc

class SessionGuard(object):
    
    def __init__ (self, func):
        self.func = func
    
    def __call__ (self, *args, **kw):
        settings = Settings()
        authenticator = args[0].authenticator

        if authenticator.connection_state() == ConnectionState.LoggedIn:
            return self.func (*args, **kw)
        else:
            xbmc.log('Not logged in. Trying to log in before proceeding...')
            result = authenticator.login(settings.username(), settings.password())
            if result == ConnectionState.LoggedIn:
                return self.func (*args, **kw)
        
        raise Exception("Cannot connect to Spotify. Are your credentials valid?")

    def __get__(self, obj, ownerClass=None):
        return types.MethodType(self, obj)