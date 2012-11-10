import threading 
import fake_wpilib as wpilib


class DriveTrain(object):
    
    TANK_TREAD =    0
    ROBOT_RADIUS = 4
    PI = 3.14
    def __init__(self, drive_train):
        self.drive_train =  drive_train
        self._lock = threading.RLock()
    def get_direction(self):
        '''
            Returns a tuple of (heading, speed, yaw) indicating 
            the robot's current desired speed/direction based on what type of 
            drive_train is being used. Where heading is an angle, Yaw is 
            degrees per time deviation. 
        '''
        with self._lock:
            if self.drive_train == 0:
                try:
                    jag1 = wpilib.DigitalModule._pwm[0].Get()
                    jag2 = wpilib.DigitalModule._pwm[1].Get()
                    #speed obtained by adding together motor speeds
                    speed = (jag1 + jag2) / 2 
                    circum = 2* DriveTrain.PI * DriveTrain.ROBOT_RADIUS
                    #Assuming that the treads are 1m away from center
                    yaw = (jag2 / circum) - (jag1/circum) 
                        
                    if speed >= 0:
                        heading = 0
                    if speed < 0:
                        heading = 180
                    
                    if speed != 0 or yaw != 0:
                        print("Jag1: " + str(jag1) + " Jag2: " + str(jag2))
                    return heading, abs(speed), yaw
                except IndexError:
                    return None
