'''
    snake_board
    
    This is the game board where different snake robots play. It should be able
    to handle multiple instances of snake robots 
'''

import tkinter as tk

class SnakeBoard(object):
    
    def __init__(self, controller, board_size):
        '''
            initializes all default values and creates 
            a board, waits for run() to be called
            to start the board
            
            controller - robot code controller class
            board_size - a tuple with values (rows, cols)
        '''
        
        self.controller = controller
        self.root = tk.Tk()
        self.root.wm_title("RobotSnake")
        self.rows, self.cols = board_size
        self.margin = 5
        self.cellSize = 30
        self.canvasWidth = 2*self.margin + self.cols*self.cellSize
        self.canvasHeight = 2*self.margin + self.rows*self.cellSize
        
        self.canvas = tk.Canvas(self.root, width=self.canvasWidth, height=self.canvasHeight)
        self.canvas.pack()
        self.root.resizable(width=0, height=0)
        
        # Store canvas in root and in canvas itself for callbacks
        self.root.canvas = self.canvas.canvas = self.canvas
        
        # Set up canvas data and call init
        self.init_canvas()
        
        # set up events
        self.root.bind("<Key>", self.key_pressed)
        self.timer_fired()
        
    def run(self):
        # and launch the thread
        self.root.mainloop()  # This call BLOCKS
         
    def timer_fired(self):
        ignoreThisTimerEvent = self.ignoreNextTimerEvent
        self.ignoreNextTimerEvent = False
        if self.isGameOver == False and ignoreThisTimerEvent == False:
            # only process timer_fired if game is not over
            self.move_robot()
            self.redraw_all()
            #draw robot position
            self.draw_snake_cell(self.robot_pos[0], self.robot_pos[1], "red")
        # whether or not game is over, call next timer_fired
        # (or we'll never call timer_fired again!)
        delay = 150 # milliseconds

    def move_robot(self):
        '''
            direction = self.controller.drive_train.get_direction()
            if direction not None:
                move_direction = direction[0]
                if move_direction >= 
                self.robot_pos += 
        '''
        pass
            
    def key_pressed(self, event):
        '''
            likely to take in a set of parameters to treat as up, down, left,
            right, likley to actually be based on a joystick event... not sure
            yet
        '''
        if event.keysym == "Up":
            self.controller.set_joystick(0, 1)
        elif event.keysym == "Down":
            self.controller.set_joystick(0, -1)
        elif event.keysym == "Left":
            self.controller.set_joystick(-1, 0)
        elif event.keysym == "Right":
            self.controller.set_joystick(1, 0)
        elif event.char == " ":
            mode = self.controller.get_mode()
            if mode == self.controller.MODE_DISABLED:
                self.controller.set_mode(self.controller.MODE_OPERATOR_CONTROL)
            else:
                self.controller.set_mode(self.controller.MODE_DISABLED)
    
    def init_canvas(self):
        '''
            initializes self.canvas to draw on
        '''
        self.load_snake_board()
        self.inDebugMode = False
        self.isGameOver = False
        self.snakeDrow = 0
        self.snakeDcol = -1 # start moving left
        self.ignoreNextTimerEvent = False
        self.redraw_all()
        
    def load_snake_board(self):
        '''
            loads the board on to the self.canvas
        '''
        self.snakeBoard = []
        for row in range(self.rows): 
            self.snakeBoard += [[0] * self.cols]
        self.spawn_robot()
        #find_snake_head(self.canvas)
        #place_food(self.canvas)
        
    def spawn_robot(self):
        '''
           Does things required to spawn a robot on to field including 
           storing its locations, location is stored as location on map
           and robots facing direction which is represented as degrees
        '''
        self.robot_pos = self.controller.robot_pos = (self.rows//2, self.cols//2,
                                                      0)
        
    def redraw_all(self):
        self.canvas.delete(tk.ALL)
        self.draw_snake_board()
        if self.isGameOver == True:
            cx = self.canvasWidth/2
            cy = self.canvasHeight/2
            self.canvas.create_text(cx, cy, text="Game Over!", font=("Helvetica", 32, "bold"))
            
    def draw_snake_board(self):
        
        rows = len(self.snakeBoard)
        cols = len(self.snakeBoard[0])
        for row in range(rows):
            for col in range(cols):
                self.draw_snake_cell(row, col, "white")

    def draw_snake_cell(self, row, col, color):
        left = self.margin + col * self.cellSize
        right = left + self.cellSize
        top = self.margin + row * self.cellSize
        bottom = top + self.cellSize
        self.canvas.create_rectangle(left, top, right, bottom, fill=color)

