import threading 
import fake_wpilib as wpilib


class DriveTrain(object):
    
    TANK_TREAD =    0
    #circumference chosen for simplicity
    ROBOT_CIRCUM = 8
    PI = 3.14
    
    def __init__(self, drive_train):
        self.drive_train =  drive_train
        self._lock = threading.RLock()
        
    def get_direction(self):
        '''
            Returns a tuple of (speed, yaw) indicating 
            the robot's current desired speed/direction based on what type of 
            drive_train is being used. Where heading is an angle, Yaw is 
            % of circle in one time deviation. 
        '''
        with self._lock:
            if self.drive_train == 0:
                try:
                    jag_r = wpilib.DigitalModule._pwm[0]
                    jag_l = wpilib.DigitalModule._pwm[1]
                    
                    jag1 = 0
                    jag2 = 0
                    
                    if jag_r is not None:
                        jag1 = -jag_r.Get()
                    
                    if jag_l is not None:
                        jag2 = jag_l.Get()

                    #speed obtained by adding together motor speeds
                    speed = (jag1 + jag2) / 2 
                    #Assuming that the treads are 1m away from center
                    yaw = (jag2 / DriveTrain.ROBOT_CIRCUM) - (jag1/DriveTrain.ROBOT_CIRCUM) 
                    
                    #if speed != 0 or yaw != 0:
                    #    print("Jag1: " + str(jag1) + " Jag2: " + str(jag2))
                    return speed, yaw
                
                except IndexError:
                    return None
