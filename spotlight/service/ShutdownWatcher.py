from threading import Thread
import xbmc
import time

class ShutdownWatcher(Thread):
       
    def __init__(self, server):
        Thread.__init__(self)
        self.server = server

    def run(self):
        while not xbmc.abortRequested:
            time.sleep(2)
        
        self.server.stop()
        
        
        
    
    