import types

from spotify import ConnectionState

from spotilight.service.util.Settings import Settings


class SessionGuard(object):
    
    MAX_TRIALS = 2
    
    def __init__ (self, func):
        self.func = func
    
    def __call__ (self, *args, **kw):
        trials = 0
        settings = Settings()
        authenticator = args[0].authenticator
        
        while not authenticator.connection_state() is ConnectionState.LoggedIn and trials < SessionGuard.MAX_TRIALS:
            authenticator.login(settings.username(), settings.password())
            trials += 1
            
        if authenticator.connection_state() is ConnectionState.LoggedIn:
            return self.func (*args, **kw)
        
        raise Exception("Cannot connect to Spotify. Are your credentials valid?")
    
    def __get__(self, obj, ownerClass=None):
        return types.MethodType(self, obj)