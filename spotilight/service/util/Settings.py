import xbmcaddon

class Settings:
    
    LABEL_TO_BITRATE = {
                        '96kbps' : 2,
                        '160kbps' :0,
                        '320bps' : 1,
                        }
    
    def __init__(self):
        self.addon = xbmcaddon.Addon("plugin.audio.spotlight")
        
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