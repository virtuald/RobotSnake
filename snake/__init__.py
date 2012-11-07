'''
    Snake
    
    This is a snake game designed to create a field,
    manage collisions, and score, robots that are
    created by students. This game is to be processed
    as time passes, not on click events.
    
'''
__all__ = ['snake_board']

from .snake_board import SnakeBoard
from . import snake_wpilib

def launch_robot(robot_module, myrobot):
    snake_board = SnakeBoard(8,16)
    snake_board.run()

