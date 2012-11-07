'''
    Generic fake_wpilib launching script for RobotSnake
    
    -> This file is copied to all robots, and should not need to be
    modified at all
'''


import sys
import os.path

# setup the path correctly for the snake package to be loaded
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import snake

# directory that robot.py is located, relative to this file
# -> this automatically sets the path to a directory above, with the same
#    directory name that this file is in
robot_path = '../%s' % os.path.split(__file__)[1][:-3]


def run_tests(robot_module, myrobot):
    snake.launch_robot(robot_module, myrobot)
