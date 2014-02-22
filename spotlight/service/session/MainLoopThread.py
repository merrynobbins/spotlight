import threading

class MainLoopThread(threading.Thread):
       
    def __init__(self, main_loop, session):
        threading.Thread.__init__(self)
        self.main_loop = main_loop
        self.session = session
    
    def run(self):
        self.main_loop.loop(self.session)
    
    def stop(self):
        self.main_loop.quit()
        self.join(10)