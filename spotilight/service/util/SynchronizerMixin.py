from threading import Event
import xbmc

class SynchronizerMixin(object):
        
    def run_and_wait(self):
        self.flag = Event()
        self.arrived = False
        result = self.execute()
        xbmc.log('Performed action. Waiting for result... [ %s ]' % self.__class__.__name__)
        self.before_wait()
                
        if self.disable_wait is not True:
            self.flag.wait(10)
        else:
            xbmc.log('Wait is not needed [ %s ]' % self.__class__.__name__)
    
        if not self.arrived and self.disable_wait is not True:    
            xbmc.log('Action timed out [ %s ]' % self.__class__.__name__)
        
        if self.arrived:
            xbmc.log('Result arrived [ %s ]' % self.__class__.__name__)
            
        self.clean_up()
        return result
    
    def done(self, result = None):       
        self.arrived = True
        self.flag.set()
        self.flag.clear()
        self.disable_wait = False;

    def disable_wait(self):
        self.disable_wait = True
        
    def before_wait(self):
        pass
    
    def clean_up(self):
        pass
        