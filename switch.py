import matplotlib.pyplot as plt
from web_screen.main import start_screen
from web_screen.matplotlib import update_screen
from web_screen.controls import keyboard

import numpy as np
import random

def_figsize = (10, 4)
def_dpi = 100
width,height = def_figsize
width,height = width*def_dpi,height*def_dpi
start_screen(width,height)
#keyboard.bind_func('ctrl',)
try:
    while True:
        print(keyboard.active('ctrl'))
        nx = random.randint(2,7)
        x = np.arange(0, nx * np.pi, 0.05)
        y_sin = np.sin(x)
        y_cos = np.cos(x)
        
        # Create a figure with 1 row and 2 columns of subplots
        fig, axs = plt.subplots(1, 2, figsize=def_figsize,dpi=def_dpi)
        
        # Plot on the first axes (left subplot)
        axs[0].plot(x, y_sin, 'b-')
        axs[0].set_title('Sine Wave')
        axs[0].set_xlabel('Angle (radians)')
        axs[0].set_ylabel('Amplitude')
        
        # Plot on the second axes (right subplot)
        axs[1].plot(x, y_cos, 'r--')
        axs[1].set_title('Cosine Wave')
        axs[1].set_xlabel('Angle (radians)')
        axs[1].set_ylabel('Amplitude')
        
        # Add a overall title for the figure and adjust layout
        fig.suptitle('Sine and Cosine Comparison')
        plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Adjust layout to prevent title overlap
    
        
        update_screen()
except:
    exit()

 