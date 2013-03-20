
# TODO: Not complete yet, this is just a bunch of ideas

import math

from .game_manager import GameManager
from .snake_elements import GameElement, DrawableElement


DEGREES = 360

class SnakeRobot(GameElement):
    
    def __init__(self, controller):
        
        super().__init__()
        
        self.controller = controller
        self.controller.robot_face = 0
        
        # create a bunch of drawable objects that represent the robot
        pts = [(100, 100), (130,100), (130,130), (100,130)]
        center = (115,115)
        
        robot = DrawableElement(pts, center, 0, 'red')
        self.elements.append(robot)
        
        
        pts = [(100, 100), (130, 115), (100, 130)]
        
        robot_pt = DrawableElement(pts, center, 0, 'green')
        self.elements.append(robot_pt)
    
    def perform_move(self):
        
        if not self.controller.is_alive():
            self.elements[1].set_color('gray')
        
        # query the controller for move information
        self.move_robot()
        
        # finally, call the superclass to actually do the drawing?
        self.update_coordinates()
        
        
    def move_robot(self):
        # TODO: rewrite this
        
        direction = None
        
        # don't move the robot in disabled mode... 
        if self.controller.get_mode() != GameManager.MODE_DISABLED:
            direction = self.controller.drive_train.get_direction()
            
        if direction is not None:
            #currently on a 2d grid board we are allowing only movement and
            #yaw in the 0, 90, 180, 270 directions
            
            # TODO: make the drivetrain return results that we don't have
            # to do more math on.. 
            
            robot_speed, robot_yaw = direction
            
            robot_yaw = robot_yaw * 80
            
            if robot_yaw != 0:
                self.rotate(robot_yaw)
            
            x = 20*robot_speed*math.cos(robot_yaw) 
            y = 20*robot_speed*math.sin(robot_yaw)
            
            self.move((x,y))
            
        '''
            #since move_direction is referencing the robot and facing
            #references the board the combined angle is the movement
            #referencing the board  
            
            move_direction =  (robot_direction + facing) % DEGREES
            if move_direction >= 0 and move_direction < 90:
                self.controller.robot_pos[1] += robot_speed
            elif move_direction >= 90 and move_direction < 180:
                self.controller.robot_pos[0] += robot_speed
            elif move_direction >= 180 and move_direction < 270:
                self.controller.robot_pos[1] -= robot_speed
            elif move_direction >= 270 and move_direction < 360:
                self.controller.robot_pos[0] -= robot_speed
            
            self.controller.robot_face = (robot_yaw * DEGREES + facing ) % DEGREES
            if robot_speed != 0 or robot_yaw !=0:
                print("Robot Facing: " + str(facing) )
                print("Robot Direction: " + str(robot_direction))
                print("Robot Speed: " + str(robot_speed))
                print("Move Direction: " + str(move_direction))
                print("Pos: " +  str(self.controller.robot_pos[0]) + ", " + 
                      str(self.controller.robot_pos[1]))
                print("Yaw: " + str(robot_yaw) )
        '''
            
        #clear joystick value
        self.controller.set_joystick(0.0, 0.0)
        
