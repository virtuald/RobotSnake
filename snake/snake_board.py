'''
    snake_board
    
    This is the game board where different snake robots play. It should be able
    to handle multiple instances of snake robots 
    
    Note: http://bugs.python.org/issue11077 seems to indicate that tk is 
    supposed to be thread-safe, but everyone else on the net insists that
    it isn't. Be safe, don't call into the GUI from another thread.  
'''

import tkinter as tk
import queue


class SnakeBoard(object):
    
    def __init__(self, game_manager, board_size):
        '''
            initializes all default values and creates 
            a board, waits for run() to be called
            to start the board
            
            game_manager - game manager class instance
            board_size - a tuple with values (rows, cols)
        '''
        
        self.game_manager = game_manager
        self.game_elements = []      # robots, walls, missles, etc
        
        self.root = tk.Tk()
        self.root.wm_title("RobotSnake")
        
        # setup mode switch
        frame = tk.Frame(self.root)
        frame.pack(side=tk.TOP, anchor=tk.W)
        
        self.mode = tk.IntVar()
        
        def _set_mode():
            self.game_manager.set_mode(self.mode.get())
        
        button = tk.Radiobutton(frame, text='Disabled', variable=self.mode, \
                                value=game_manager.MODE_DISABLED, command=_set_mode)
        button.pack(side=tk.LEFT)
        button = tk.Radiobutton(frame, text='Autonomous', variable=self.mode, \
                                value=game_manager.MODE_AUTONOMOUS, command=_set_mode)
        button.pack(side=tk.LEFT)
        button = tk.Radiobutton(frame, text='Teleoperated', variable=self.mode, \
                                value=game_manager.MODE_OPERATOR_CONTROL, command=_set_mode)
        button.pack(side=tk.LEFT)
        
        # setup board characteristics
        self.rows, self.cols = board_size
        self.margin = 5
        self.cellSize = 30
        self.canvasWidth = 2*self.margin + self.cols*self.cellSize
        self.canvasHeight = 2*self.margin + self.rows*self.cellSize
        
        self.canvas = tk.Canvas(self.root, width=self.canvasWidth, height=self.canvasHeight)
        self.canvas.pack()
        self.root.resizable(width=0, height=0)
        
        self.text_id = None
        
        # Store canvas in root and in canvas itself for callbacks
        self.root.canvas = self.canvas.canvas = self.canvas
        
        # Set up canvas data and call init
        self.init_canvas()
        
        # Set up invoke
        self.queue = queue.Queue()
        self.root.bind('<<Idle>>', self._on_idle)
        
        # set up events
        self.root.bind("<Key>", self.key_pressed)
        
        # connect to the controller
        self.game_manager.on_mode_change(lambda mode: self.idle_add(self.on_robot_mode_change, mode))
        
        self.timer_fired()
        
    def idle_add(self, callable, *args):
        '''Call this with a function as the argument, and that function
           will be called on the GUI thread via an event
           
           This function returns immediately
        '''
        self.queue.put((callable, args))
        self.root.event_generate('<<Idle>>', when='tail')
        
    def _on_idle(self, event):
        '''This should never be called directly, it is called via an 
           event, and should always be on the GUI thread'''
        while True:
            try:
                callable, args = self.queue.get(block=False)
            except queue.Empty:
                break
            callable(*args)
        
    def add_game_element(self, element):
        '''Add elements to the board'''
        
        element.initialize(self.canvas)
        self.game_elements.append(element)
        
    def run(self):
        # and launch the thread
        self.root.mainloop()  # This call BLOCKS
         
    def timer_fired(self):
        
        if self.isGameOver == False:
            # only process timer_fired if game is not over
            self.move_objects()
            
        # whether or not game is over, call next timer_fired
        # (or we'll never call timer_fired again!)
        delay = 150 # milliseconds
        self.canvas.after(delay, self.timer_fired) # pause, then call timerFired again
        
        
    def move_objects(self):
        
        # TODO: process collisions and such too
        
        for element in self.game_elements:
            element.perform_move()
        
    def key_pressed(self, event):
        '''
            likely to take in a set of parameters to treat as up, down, left,
            right, likely to actually be based on a joystick event... not sure
            yet
        '''
        
        if event.keysym == "Up":
            self.game_manager.set_joystick(0, 1, 0)      # robot 0
        elif event.keysym == "Down":
            self.game_manager.set_joystick(0, -1, 0)     # robot 0
        elif event.keysym == "Left":
            self.game_manager.set_joystick(1, 0, 0)      # robot 0
        elif event.keysym == "Right":
            self.game_manager.set_joystick(-1, 0, 0)     # robot 0
            
        #elif event.keysym == "w":
        #    self.game_manager.set_joystick(0, 1, 1)      # robot 1
        #elif event.keysym == "s":
        #    self.game_manager.set_joystick(0, -1, 1)     # robot 1
        #elif event.keysym == "a":
        #    self.game_manager.set_joystick(1, 0, 1)      # robot 1
        #elif event.keysym == "d":
        #    self.game_manager.set_joystick(-1, 0, 1)     # robot 1
            
        elif event.char == " ":
            mode = self.game_manager.get_mode()
            if mode == self.game_manager.MODE_DISABLED:
                self.game_manager.set_mode(self.game_manager.MODE_OPERATOR_CONTROL)
            else:
                self.game_manager.set_mode(self.game_manager.MODE_DISABLED)
    
    def init_canvas(self):
        '''
            initializes canvas to draw on
        '''
        
        self.draw_snake_board()
        self.isGameOver = False
        self.draw_snake_board()
        self.draw_mode_text()
        
    def draw_mode_text(self):
        
        text = None
        
        if self.isGameOver == True:
            text = "Game Over!"
        elif not self.game_manager.is_alive():
            text = "ROBOT DIED"
        elif self.game_manager.get_mode() == self.game_manager.MODE_DISABLED:
            text = "ROBOT DISABLED"
        
        if self.text_id is not None:
            self.canvas.delete(self.text_id)
            self.text_id = None
        
        if text is not None:
            cx = self.canvasWidth/2
            cy = self.canvasHeight/2
            self.text_id = self.canvas.create_text(cx, cy, text=text, font=("Helvetica", 32, "bold"))
        
            
    def draw_snake_board(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.draw_board_cell(row, col, "white")
            
    def draw_board_cell(self, row, col, color):
        left = self.margin + col * self.cellSize
        right = left + self.cellSize
        top = self.margin + row * self.cellSize
        bottom = top + self.cellSize
        self.canvas.create_rectangle(left, top, right, bottom, fill=color)        
        
    def on_robot_mode_change(self, mode):
        self.mode.set(mode)
        self.draw_mode_text()
