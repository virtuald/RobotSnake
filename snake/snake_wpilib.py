'''
    Replaces any portions of fake_wpilib that need to be different
    for the snake game
    
    In particular, time needs to be different
'''

import time
import threading

import fake_wpilib as wpilib
import fake_wpilib.fake_time


class FakeTime(object):
    
    def __init__(self):
        self.time = 0
        self.notifiers = []

    def Get(self):
        return time.time()
        
    def IncrementTimeBy(self, secs):
        time.sleep(sec)
    
    def AddNotifier(self, notifier):
        # todo: use threads to implement these
        raise RuntimeError("TODO: Implement this")
        
        if notifier not in self.notifiers:
            notifier.run_time = self.time + notifier.m_period
            self.notifiers.append( notifier )
    
    def RemoveNotifier(self, notifier):
        # todo: use threads to implement these
        raise RuntimeError("TODO: Implement this")
    
        if notifier in self.notifiers:
            self.notifiers.remove( notifier )

fake_wpilib.fake_time.FAKETIME = FakeTime()




