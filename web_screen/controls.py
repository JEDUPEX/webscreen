"""from pyvirtualdisplay.display import Display
import Xlib.display"""
import os
from datetime import datetime, timedelta

max_time = timedelta(milliseconds=200)
def time_check(info):
    time = info[1]
    diff = datetime.now() - time
    return diff <= max_time
    
class Keyboard():
    def __init__(self):
        self._active = {}
        self._bound_funcs = {}
        
    def active(self,key):
        return key in self._active
        
    def press(self,key):
        self._active[key] = datetime.now()
        
    def bind_func(self,key,func):
        self._bound_funcs[key] = func
        
    def process_bindings(self):
        for key,_func in self._bound_funcs.items():
            if self.active(key):
                _func()
    def reset(self):
        self._active = dict(filter(time_check,self._active.items()))
                
class Mouse():
    def __init__(self,width,height):
        self.screen_width = width
        self.screen_height = height
        self.posx = width/2
        self.posy = height/2
        self._active = {}
        self._bound_funcs = {}
        
    def active(self,key):
        return key in self._active
        
    def click(self,key):
        self._active[key] = datetime.now()
        
    def bind_func(self,key,func):
        self._bound_funcs[key] = func
        
    def process_bindings(self):
        for key,_func in self._bound_funcs.items():
            if self.active(key):
                _func()
    
    def move(self,x,y):
        sx = self.screen_width
        sy = self.screen_height
        
        nx = x if x >= 0 else 0
        nx = x if x <= sx else sx
        
        ny = y if y >= 0 else 0
        ny = y if y <= sy else sy
        
        self.posx = nx
        self.posy = ny
        
    def reset(self):
        self._active = dict(filter(time_check,self._active.items()))
                

mouse = Mouse(0,0)
keyboard = Keyboard()
def configure(width,height):
    mouse.screen_width = width
    mouse.screen_height = height
    mouse.posx = width/2
    mouse.posy = height/2
    """
    disp = Display(visible=True, size=(width, height), backend="xvfb", use_xauth=True)
    disp.start()
    
    import pyautogui
    # Provide the path to the virtual display to PyAutoGUI (if necessary)
    pyautogui._pyautogui_x11._display = Xlib.display.Display(os.environ['DISPLAY'])
    """

async def process_input(actions):
    keyboard.reset()
    mouse.reset()
    keyboard_actions = actions['keyboard']
    mouse_actions = actions['mouse']
    for k_act in keyboard_actions:
        keyboard.press(k_act)
    for m_act in mouse_actions:
        if m_act['type'] == 'move':
            mouse.move(m_act['x'],m_act['y'])
        elif m_act['type'] == 'click':
            mouse.click(m_act['key'])
            
    mouse.process_bindings()
    keyboard.process_bindings()
    """pyautogui.hotkey('ctrl', 'c') # Simulates Ctrl+C"""
    