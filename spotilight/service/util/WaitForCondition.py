import time

class WaitForCondition:
    
    TRIALS = 70
    
    def __init__(self, condition, trials = TRIALS):
        self.condition = condition
        self.trials = trials
        self.wait()
        
    def wait(self):
        loops = 0
        while not self.condition() and loops < self.trials:
            time.sleep(0.1)
            loops += 1
            