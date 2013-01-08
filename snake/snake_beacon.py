
# TODO: Not complete yet, this is just a bunch of ideas

import math
import time

from .game_manager import GameManager
from .snake_elements import GameElement, DrawableElement
import fake_wpilib as wpilib

import random

DEGREES = 360

class SnakeBeacon(GameElement):
    
    def __init__(self, controller, snake_robot):
        
        super().__init__()
        
        self.controller = controller
        self.controller.robot_face = 0
        
        # create a drawable object for the beacon
        self.half = False
        self.beacon = DrawableElement(None, None, 0, 'orange')
        self.elements.append(self.beacon)
        
        self.robot = snake_robot
        self.blink_time = time.time()
        self.ticks = 0
        self.score = 0
        
        self.generate_coordinates()
        
    def generate_coordinates(self):
        
        if self.half == True:
            # rand a center point between 300-600, 0-200
            x = int(random.uniform(10,230))
            y = int(random.uniform(10,250))
        else:
            x = int(random.uniform(250,480))
            y = int(random.uniform(10, 250))
        
        self.beacon.pts = [(x-5, y-5), (x+5,y-5), (x+5,y+5), (x-5,y+5)]
        self.beacon.center = (x, y)
        self.half = not self.half
        self.beacon.update_coordinates()
    
    def perform_move(self):
        
        # do calculation here
        rx, ry = self.robot.elements[0].center
        sx, sy = self.elements[0].center
        
        distance = math.hypot(sx-rx, sy-ry)
        
        channel = wpilib.AnalogModule._channels[4]
        if channel is not None:            
            channel.value = distance
            
        # hehe.
        mode = self.robot.controller.get_mode()
        if mode  != GameManager.MODE_DISABLED:
            if distance < 20:
                self.generate_coordinates()
                self.ticks = 0
                
                if mode == GameManager.MODE_AUTONOMOUS:
                    self.score += 1
                    print("Point scored! Current score is %s" % self.score)
           
            # hehehe.
            self.ticks += 1
            if self.ticks == 60:
                if self.robot.controller.is_alive():
                    self.robot.controller.stop()
                    print("Robot has been terminated by The Beacon.")
                    print("Score: %s" % self.score) 
        
        self.blink()        
        
    def blink(self):
        
        t = time.time()
        if t - self.blink_time > 0.5:
            if self.beacon.color == 'orange':
                self.beacon.set_color('red')
            else:
                self.beacon.set_color('orange')
            self.blink_time = t
