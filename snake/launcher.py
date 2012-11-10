

from .snake_board import SnakeBoard
from .controller import RobotController


def launch_robot(robot_module, myrobot, board_size=(8,16)):
    '''
        Creates a robot controller, a board, and sets things up
    '''
    
    # create the robot controller
    controller = RobotController(robot_module, myrobot)
    
    # start the robot controller (does not block)
    controller.run()
    
    # create the board 
    snake_board = SnakeBoard(controller, board_size)
    

    
    # launch the board last (blocks until game is over)
    snake_board.run()

    # once it has finished, try to shut the robot down
    # -> if it can't, then the user messed up
    if not controller.stop():
        print('Error: could not stop the robot code! Check your code')