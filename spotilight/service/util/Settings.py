import xbmcaddon

class Settings:
    
    def __init__(self):
        self.addon = xbmcaddon.Addon("plugin.audio.spotifyxbmcplugin")
        
    def username(self):
        return self.addon.getSetting('username')
    
    def password(self):
        return self.addon.getSetting('password')
    
    