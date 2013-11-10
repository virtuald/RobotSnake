

try:
    import wpilib
except ImportError:
    import fake_wpilib as wpilib


stick1 = wpilib.Joystick(1)

# control components
l_motor_pwm_ch = 1
r_motor_pwm_ch = 2

l_driveMotor    = wpilib.Jaguar(l_motor_pwm_ch)
r_driveMotor    = wpilib.Jaguar(r_motor_pwm_ch)

drive           = wpilib.RobotDrive(l_driveMotor, r_driveMotor)
    
class MyRobot(wpilib.SimpleRobot):

    def __init__(self):
        '''Constructor'''
        
        wpilib.SimpleRobot.__init__(self)
        
    def Autonomous(self):
    
        print("MyRobot::Autonomous()")
    
        while self.IsAutonomous() and self.IsEnabled():
            wpilib.Wait(0.01)
    
            
    def Disabled(self):
        
        print("MyRobot::Disabled()")
    
        while self.IsDisabled():
            wpilib.Wait(0.01)
        
    
    def OperatorControl(self):
        '''Called during Teleoperated Mode'''
    
        print("MyRobot::OperatorControl()")
        
        watchdogTimeout = 0.25
        dog = self.GetWatchdog()
        dog.SetEnabled(True)
        dog.SetExpiration(watchdogTimeout)
        
        while self.IsOperatorControl() and self.IsEnabled():

            dog.Feed()
            
            drive.ArcadeDrive(stick1.GetY(), stick1.GetX(), False)
            
            wpilib.Wait(0.05)
            
        dog.SetEnabled(False)
    
    
def run():
    '''This function must be present for the robot to start'''
    robot = MyRobot()
    robot.StartCompetition()
    
    # must return a value to work with the tester program
    return robot

