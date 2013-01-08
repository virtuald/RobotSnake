
# TODO: Not complete yet, this is just a bunch of ideas

import math

from .snake_elements import GameElement, DrawableElement
import fake_wpilib as wpilib

import random

DEGREES = 360

class SnakeBeacon(GameElement):
    
    def __init__(self, controller, snake_robot):
        
        super().__init__()
        
        self.controller = controller
        self.controller.robot_face = 0
        
        # rand a center point between 300-600, 0-200
        x = int(random.uniform(200,480))
        y = int(random.uniform(50, 250))
        
        # create a bunch of drawable objects that represent the robot
        pts = [(x-5, y-5), (x+5,y-5), (x+5,y+5), (x-5,y+5)]
        center = (x, y)
        
        beacon = DrawableElement(pts, center, 0, 'orange')
        self.elements.append(beacon)
        
        self.robot = snake_robot
    
    def perform_move(self):
        
        # do calculation here
        rx, ry = self.robot.elements[0].center
        sx, sy = self.elements[0].center
        
        distance = math.hypot(sx-rx, sy-ry)
        
        channel = wpilib.AnalogModule._channels[4]
        if channel is not None:            
            channel.value = distance
        
        
