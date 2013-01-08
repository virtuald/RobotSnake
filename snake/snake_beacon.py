
# TODO: Not complete yet, this is just a bunch of ideas

import math
import time

from .game_manager import GameManager
from .snake_elements import GameElement, DrawableElement
import fake_wpilib as wpilib

import random

DEGREES = 360

quotes = [
    "All your base are belong to us",
    "Drown the kids and shoot the neighbors! We've got a winner!",
    '*evil chuckle* No Mr. Bond I expect you to die.',
    'Have you ever danced with the devil in the pale moonlight?',
    "I'll cut your heart out with a spoon",
    "I'll get you my pretty. And your little dog too.",
    "I'm going to enjoy watching you die,",
    "I'm here to kill you. Is this a bad time?",
    "It's a wonderful plan, isn't it? Everyone dies and I profit.",
    "It's that stupid frog...kissed any princesses lately?",
    "Nothing can beat the music of hundreds of voices screaming in unison.",
    "The weak always strive to be weaker...",
    "Wait, do you hear that? It's the sound of the Reaper calling your name.",
    'Wanna know how I got these scars?',
    "What fun is destruction if no precious lives are lost?",
    "What? Not laughing yet? Just wait til I get to the punch line. It'll kill you! HaHaHaHaHaHaHaHa",
    "You can run but you're still going to die!",
    "You don't matter! In fact, in a few seconds, you won't even be matter.",    
    "You gonna get whacked, 'cuz you're weak.",
    "You play with fire, you get burned",
    "You shall suffer! You shall all suffer!",
    "Your death is inevitable, you cannot escape it",
    ]

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
                print("The Beacon: Fools! You'll never destroy me!")
                self.generate_coordinates()
                self.ticks = 0
                
                if mode == GameManager.MODE_AUTONOMOUS:
                    self.score += 1
                    print("Point scored! Current score is %s" % self.score)
           
            # hehehe.
            self.ticks += 1
            if self.ticks == 10:
                print("The Beacon: %s" % quotes[random.randint(0, len(quotes)-1)])
            elif self.ticks == 30:
                print("The Beacon: %s" % quotes[random.randint(0, len(quotes)-1)])
            elif self.ticks == 50:
                print("The Beacon: Beware you fools.........the hour has come!")
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
