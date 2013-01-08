'''
    This manages the active state of the robot
''' 

import sys
import threading
import time

import fake_wpilib as wpilib
import _wpilib
from .drive_train import DriveTrain
from .game_manager import GameManager

class RobotController(object):
    
    def __init__(self, robot_module, myrobot):
    
        self.mode = GameManager.MODE_DISABLED
        self.mode_callback = None
    
        self.robot_module = robot_module
        self.myrobot = myrobot
        self.drive_train = DriveTrain(DriveTrain.TANK_TREAD)
        
        # attach to the robot
        _wpilib.internal.on_IsEnabled = self.on_IsEnabled
        _wpilib.internal.on_IsAutonomous = self.on_IsAutonomous
        _wpilib.internal.on_IsOperatorControl = self.on_IsOperatorControl
        
        # any data shared with the snake board must be protected by
        # this since it's running in a different thread
        self._lock = threading.RLock()
        
        self.thread = threading.Thread(target=self._robot_thread)
        
    def run(self):
        self._run_code = True
        self.thread.start()
        
    def stop(self):
        with self._lock:
            self._run_code = False
        
            # if the robot code is spinning in any of the modes, then
            # we need to change the mode so it returns back to us
            if self.mode == GameManager.MODE_DISABLED:
                self.mode = GameManager.MODE_OPERATOR_CONTROL
            else:
                self.mode = GameManager.MODE_DISABLED
        
        try:
            self.thread.join(timeout=5.0)
        except RuntimeError:
            return False
        
        return not self.thread.is_alive()
        
    #
    # API used by the SnakeBoard class
    #
    
    def is_alive(self):
        return self.thread.is_alive()
    
    def on_mode_change(self, callable):
        '''When the robot mode changes, call the function with the mode'''
        with self._lock:
            self.mode_callback = callable
    
    def set_joystick(self, x, y):
        '''
            Receives joystick values from the SnakeBoard
        '''
        with self._lock:
            drive_stick = self.driver_station.sticks[0]
            drive_stick[1] = x
            drive_stick[2] = y
            
    def set_mode(self, mode):
        
        if mode not in [GameManager.MODE_DISABLED, 
                        GameManager.MODE_AUTONOMOUS, 
                        GameManager.MODE_OPERATOR_CONTROL]:
            raise ValueError("Invalid value for mode: %s" % mode)
        
        with self._lock:
            
            # TODO: need a way to notify the caller that the set failed. Perhaps an exception?
            if not self.is_alive():
                return
            
            old_mode = self.mode
            self.mode = mode
            callback = self.mode_callback
            
        # don't call from inside the lock
        if old_mode != mode and callback is not None:
            callback(mode)

    def get_mode(self):
        with self._lock:
            return self.mode

    #
    # Runs the code
    #
    
    def _check_sleep(self, idx):
        '''This ensures that the robot code called Wait() at some point'''
        
        # TODO: There are some cases where it would be ok to do this... 
        if not wpilib.fake_time.FAKETIME.slept[idx]:
            errstr = '%s() function is not calling wpilib.Wait() in its loop!' % self.mode_map[self.mode]
            raise RuntimeError(errstr)
            
        wpilib.fake_time.FAKETIME.slept[idx] = False
        
    
    def on_IsEnabled(self):
        with self._lock:
            self._check_sleep(0)
            return self.mode != GameManager.MODE_DISABLED
        
    def on_IsAutonomous(self, tm):
        with self._lock:
            self._check_sleep(1)
            if not self._run_code:
                return False
            return self.mode == GameManager.MODE_AUTONOMOUS
        
    def on_IsOperatorControl(self, tm):
        with self._lock:
            self._check_sleep(2)
            if not self._run_code:
                return False
            return self.mode == GameManager.MODE_OPERATOR_CONTROL
            
    def on_WatchdogError(self, last_fed, period, expiration):
        print('WATCHDOG FAILURE! Last fed %0.3f seconds ago (expiration: %0.3f seconds)' % 
                                  (period, expiration), file=sys.stderr)
        self.set_mode(GameManager.MODE_DISABLED)
    
    def _robot_thread(self):
        
        # setup things for the robot
        self.driver_station = wpilib.DriverStation.GetInstance()
        self.myrobot.watchdog.error_handler = self.on_WatchdogError
        
        last_mode = None
        
        try:
            while True:
                with self._lock:
                
                    mode = self.mode
                
                    if not self._run_code:
                        break
                    
                # Detect if the code is implemented improperly
                # -> This error occurs if the robot returns from one of its 
                #    functions for any reason other than a mode change, as 
                #    this is the only acceptable reason for this to occur
                if last_mode is not None:
                    if last_mode == mode:                        
                        errstr = '%s() function returned before the mode changed' % GameManager.mode_map[last_mode]
                        raise RuntimeError(errstr)
                    
                # reset this, just in case
                wpilib.fake_time.FAKETIME.slept = [True]*3
                
                if mode == GameManager.MODE_DISABLED:
                    self.myrobot.Disabled()
                elif mode == GameManager.MODE_AUTONOMOUS:
                    self.myrobot.Autonomous()
                elif mode == GameManager.MODE_OPERATOR_CONTROL:
                    self.myrobot.OperatorControl()
                    
                # make sure infinite loops don't kill the processor... 
                time.sleep(0.001)
                last_mode = mode
        
        finally:
            self.myrobot.GetWatchdog().SetEnabled(False)
            self.set_mode(GameManager.MODE_DISABLED)
