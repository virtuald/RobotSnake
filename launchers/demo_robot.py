
# directory that robot.py is located, relative to this file
robot_path = '../demorobot'

import run_test
snake = run_test.wpilib.load_module('snake', '/snake/__init__.py')
def run_tests(robot_module, myrobot):
    snake.launch_robot(robot_module, myrobot)
