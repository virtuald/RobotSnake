'''
    snake_board
    
    This is the game board where different snake robots play. It should be able
    to handle multiple instances of snake robots 
'''

from tkinter import *

class SnakeBoard(object):
    
    def __init__(self, rows, cols):
        '''
            initializes all default values and creates 
            a board, waits for run() to be called
            to start the board
        '''
        self.root = Tk()
        self.margin = 5
        self.cellSize = 30
        self.canvasWidth = 2*self.margin + cols*self.cellSize
        self.canvasHeight = 2*self.margin + rows*self.cellSize
        self.rows = rows
        self.cols = cols
        
        self.canvas = Canvas(self.root, width=self.canvasWidth, height=self.canvasHeight)
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
        '''
            I think this should be called externally in an Update function
        '''
        ignoreThisTimerEvent = self.ignoreNextTimerEvent
        self.ignoreNextTimerEvent = False
        if ((self.isGameOver == False) and
            (ignoreThisTimerEvent == False)):
            # only process timer_fired if game is not over
            #move_snake(self.canvas, self.drow, self.dcol)
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
        self.snakeBoard = [ ]
        for row in range(self.rows): 
            self.snakeBoard += [[0] * self.cols]
        
        #find_snake_head(self.canvas)
        #place_food(self.canvas)
        
    def redraw_all(self):
        self.canvas.delete(ALL)
        self.draw_snake_board()
        if (self.isGameOver == True):
            cx = self.canvasWidth/2
            cy = self.canvasHeight/2
            self.canvas.create_text(cx, cy, text="Game Over!", font=("Helvetica", 32, "bold"))
            
    def draw_snake_board(self):
        
        rows = len(self.snakeBoard)
        cols = len(self.snakeBoard[0])
        for row in range(rows):
            for col in range(cols):
                self.draw_snake_cell(row, col)

    def draw_snake_cell(self, row, col):
        left = self.margin + col * self.cellSize
        right = left + self.cellSize
        top = self.margin + row * self.cellSize
        bottom = top + self.cellSize
        self.canvas.create_rectangle(left, top, right, bottom, fill="white")


