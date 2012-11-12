'''
    This manages the active state of the robot
''' 

import sys
import threading

import fake_wpilib as wpilib
from .drive_train import DriveTrain

class RobotController(object):

    MODE_DISABLED = 0
    MODE_AUTONOMOUS = 1
    MODE_OPERATOR_CONTROL = 2
    
    def __init__(self, robot_module, myrobot):
    
        self.mode = RobotController.MODE_DISABLED
        self.mode_callback = None
    
        self.robot_module = robot_module
        self.myrobot = myrobot
        self.drive_train = DriveTrain(DriveTrain.TANK_TREAD)
        
        # attach to the robot
        self.myrobot.on_IsEnabled = self.on_IsEnabled
        self.myrobot.on_IsAutonomous = self.on_IsAutonomous
        self.myrobot.on_IsOperatorControl = self.on_IsOperatorControl
        
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
            if self.mode == RobotController.MODE_DISABLED:
                self.mode = RobotController.MODE_OPERATOR_CONTROL
            else:
                self.mode = RobotController.MODE_DISABLED
        
        try:
            self.thread.join(timeout=5.0)
        except RuntimeError:
            return False
        
        return not self.thread.is_alive()
        
    #
    # API used by the SnakeBoard class
    #
    
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
        
        if mode not in [RobotController.MODE_DISABLED, 
                        RobotController.MODE_AUTONOMOUS, 
                        RobotController.MODE_OPERATOR_CONTROL]:
            raise ValueError("Invalid value for mode: %s" % mode)
        
        with self._lock:
            self.mode = mode
            callback = self.mode_callback
            
        # don't call from inside the lock
        callback(mode)

    def get_mode(self):
        with self._lock:
            return self.mode

    #
    # Runs the code
    #
    
    def on_IsEnabled(self):
        with self._lock:
            return self.mode != RobotController.MODE_DISABLED
        
    def on_IsAutonomous(self, tm):
        with self._lock:
            if not self._run_code:
                return False
            return self.mode == RobotController.MODE_AUTONOMOUS
        
    def on_IsOperatorControl(self, tm):
        with self._lock:
            if not self._run_code:
                return False
            return self.mode == RobotController.MODE_OPERATOR_CONTROL
            
    def on_WatchdogError(self, last_fed, period, expiration):
        print('WATCHDOG FAILURE! Last fed %0.3f seconds ago (expiration: %0.3f seconds)' % 
                                  (period, expiration), file=sys.stderr)
        self.set_mode(RobotController.MODE_DISABLED)
    
    def _robot_thread(self):
        
        # setup things for the robot
        self.driver_station = wpilib.DriverStation.GetInstance()
        self.myrobot._watchdog.error_handler = self.on_WatchdogError
        
        while True:
            with self._lock:
            
                mode = self.mode
            
                if not self._run_code:
                    break
                    
            # TODO: Catch robot exceptions and tell the user about it, while
            # handling it correctly in the GUI
                
            # TODO: Print status indicating what's happening here
                
            if mode == RobotController.MODE_DISABLED:
                self.myrobot.Disabled()
            elif mode == RobotController.MODE_AUTONOMOUS:
                self.myrobot.Autonomous()
            elif mode == RobotController.MODE_OPERATOR_CONTROL:
                self.myrobot.OperatorControl()
        
