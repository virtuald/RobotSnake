import threading 
import fake_wpilib
class DriveTrain(object):
    
    TANK_TREAD =    0
    ROBOT_RADIUS = 1
    PI = 3.14
    def __init__(self, drive_train):
        self.drive_train =  drive_train
        self._lock = threading.RLock()
    def get_direction(self):
        '''
            Returns a tuple of (heading, speed, yaw) indicating 
            the robot's current desired speed/direction based on what type of 
            drive_train is being used. Where heading is an angle, Yaw is 
            radians per time deviation, 
        '''
        with self._lock:
            if self.drive_train == 0:
                try:
                    can1 = fakewpilib.CAN._devices[0].Get()
                    can2 = fakewpilib.CAN._devices[1].Get()
                    #speed obtained by adding together motor speeds
                    speed = can1 + can2
                    #Assuming that the treads are 1m away from center
                    yaw = ( 2 * PI * ROBOT_RADIUS) / speed
                    if speed >= 0:
                        heading = 0
                    if speed < 0:
                        heading = 180
                    return heading, speed, yaw
                except IndexError:
                    return None
                    