import fake_wpilib as wpilib

class MyRobot(wpilib.SimpleRobot):
    '''
        demo of functioning snake bot
    '''
     
    def __init__(self):
        pass
    
    def Disabled(self):
        pass
     
    def Autonomous(self):
        pass
         
     
def run(): 
    
    '''This function must be present for the robot to start'''
    robot = MyRobot()
    robot.StartCompetition()
    return robot