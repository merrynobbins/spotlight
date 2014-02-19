from threading import Event
import xbmc

class Synchronizer:
    
    def __init__(self, command):
        self.command = command;
        self.command.set_synchronizer(self)
        self.flag = Event()
        
    def execute(self):
        result = self.command.perform()
        xbmc.log('Performed action. Waiting for result...')
        self.flag.wait(10)
        xbmc.log('Result arrived')
        return result
    
    def done(self, result):
        self.flag.set()
        self.flag.clear()
    
    
        