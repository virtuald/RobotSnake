'''
    snake_board
    This is the game board where different snake robots play. It should be able
    to handle multiple instances of snake robots 
'''
from threading import Thread
from tkinter import *

thread_num = 0  

class SnakeBoard(Thread):
    
    def __init__(self, rows, cols):
        '''
            initializes all default values and creates 
            a board, waits for run() to be called
            to start the board
        '''
        self.root = Tk()
        margin = 5
        cellSize = 30
        canvasWidth = 2*margin + cols*cellSize
        canvasHeight = 2*margin + rows*cellSize
        self.canvas = Canvas(self.root, width=canvasWidth, height=canvasHeight)
        self.canvas.pack()
        self.root.resizable(width=0, height=0)
        # Store canvas in root and in canvas itself for callbacks
        self.root.canvas = self.canvas.canvas = self.canvas
        # Set up canvas data and call init
        self.canvas.data = { }
        self.canvas.data["margin"] = margin
        self.canvas.data["cellSize"] = cellSize
        self.canvas.data["self.canvasWidth"] = canvasWidth
        self.canvas.data["self.canvasHeight"] = canvasHeight
        self.canvas.data["rows"] = rows
        self.canvas.data["cols"] = cols
        self.init_canvas()
        # set up events
        self.root.bind("<Key>", self.key_pressed)
        self.timer_fired()
        Thread.__init__(self)
        
    def run(self):
         # and launch the thread
         self.root.mainloop()  # This call BLOCKS
         
    def timer_fired(self):
        '''
            I think this should be called externally in an Update function
        '''
        ignoreThisTimerEvent = self.canvas.data["ignoreNextTimerEvent"]
        self.canvas.data["ignoreNextTimerEvent"] = False
        if ((self.canvas.data["isGameOver"] == False) and
            (ignoreThisTimerEvent == False)):
            # only process timer_fired if game is not over
            drow = self.canvas.data["snakeDrow"]
            dcol = self.canvas.data["snakeDcol"]
            #move_snake(self.canvas, drow, dcol)
            self.redraw_all()
        # whether or not game is over, call next timer_fired
        # (or we'll never call timer_fired again!)
        delay = 150 # milliseconds

    def key_pressed(self):
        '''
            likely to take in a set of parameters to treat as up, down, left,
            right, likley to actually be based on a joystick event... not sure
            yet
        '''
        pass
    
    def start_board(self):
        '''
            starts the board, this is a blocking function and should usually
            be called as a separate thread
        '''
        root.mainloop()   
    
    def init_canvas(self):
        '''
            inits self.canvas to draw on
        '''
        self.load_snake_board()
        self.canvas.data["inDebugMode"] = False
        self.canvas.data["isGameOver"] = False
        self.canvas.data["snakeDrow"] = 0
        self.canvas.data["snakeDcol"] = -1 # start moving left
        self.canvas.data["ignoreNextTimerEvent"] = False
        self.redraw_all()
        
    def load_snake_board(self):
        '''
            loads the board on to the self.canvas
        '''
        rows = self.canvas.data["rows"]
        cols = self.canvas.data["cols"]
        snakeBoard = [ ]
        for row in range(rows): snakeBoard += [[0] * cols]
        self.canvas.data["snakeBoard"] = snakeBoard
        #find_snake_head(self.canvas)
        #place_food(self.canvas)
        
    def redraw_all(self):
        self.canvas.delete(ALL)
        self.draw_snake_board()
        if (self.canvas.data["isGameOver"] == True):
            cx = self.canvas.data["self.canvasWidth"]/2
            cy = self.canvas.data["self.canvasHeight"]/2
            self.canvas.create_text(cx, cy, text="Game Over!", font=("Helvetica", 32, "bold"))
            
    def draw_snake_board(self):
        snakeBoard = self.canvas.data["snakeBoard"]
        rows = len(snakeBoard)
        cols = len(snakeBoard[0])
        for row in range(rows):
            for col in range(cols):
                self.draw_snake_cell(snakeBoard, row, col)

    def draw_snake_cell(self, snakeBoard, row, col):
        margin = self.canvas.data["margin"]
        cellSize = self.canvas.data["cellSize"]
        left = margin + col * cellSize
        right = left + cellSize
        top = margin + row * cellSize
        bottom = top + cellSize
        self.canvas.create_rectangle(left, top, right, bottom, fill="white")


