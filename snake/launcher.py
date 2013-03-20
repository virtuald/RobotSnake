
from .game_manager import GameManager
from .robot_controller import RobotController
from .snake_board import SnakeBoard
from .snake_robot import SnakeRobot
from .snake_beacon import SnakeBeacon

def launch_robot(robot_module, myrobot, board_size=(8,16)):
    '''
        Creates a robot controller, a board, and sets things up
    '''
    
    game_manager = GameManager()
    
    # create the robot controller
    controller = RobotController(robot_module, myrobot)
    
    # add it to the manager
    game_manager.add_robot(controller)
    
    # create the robot
    snake_robot = SnakeRobot(controller) 
    
    #snake_beacon = SnakeBeacon(controller, snake_robot)
    
    # start the robot controller (does not block)
    controller.run()
    
    # create the board 
    snake_board = SnakeBoard(game_manager, board_size)
    snake_board.add_game_element(snake_robot)
    #snake_board.add_game_element(snake_beacon)
    

    
    # launch the board last (blocks until game is over)
    snake_board.run()

    # once it has finished, try to shut the robot down
    # -> if it can't, then the user messed up
    if not controller.stop():
        print('Error: could not stop the robot code! Check your code')