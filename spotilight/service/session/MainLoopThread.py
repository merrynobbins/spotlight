import threading

class MainLoopThread(threading.Thread):
    __mainloop = None
    __session = None
    __proxy = None
    
    
    def __init__(self, mainloop, session):
        threading.Thread.__init__(self)
        self.__mainloop = mainloop
        self.__session = session
    
    
    def run(self):
        self.__mainloop.loop(self.__session)
    
    
    def stop(self):
        self.__mainloop.quit()
        self.join(10)