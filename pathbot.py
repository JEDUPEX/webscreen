import pygame
import sys
import random
import os
import math
from web_screen.main import start_screen
from web_screen.pygame import update_screen
from web_screen.controls import keyboard

WINDOW_WIDTH = 620
WINDOW_HEIGHT = 480

BLOCKS = {
    0:'empty',
    1:'solid',
    2:'goal'
    
}
BLOCK_LIMITS = {
    2: 1
}
BLOCK_PERCENT = {
    0:70,
    1:30
}
MAP_OPTION_SET = {0:'visible',1:'hidden',2:'unknown'}
def unwrap(data:str,step:int):
    out:list = []
    for x in range(0,len(data),step):
        out.append(data[x:x+step]) 
    return out
    
class RGB:
    r = 0 
    g = 0 
    b = 0 
    def __init__(self,r,g,b):
        self.r = r
        self.g = g 
        self.b = b
    def __str__(self):
        return f"RGB({self.r},{self.g},{self.b})"
        
    def __raw__(self):
        return (self.r,self.g,self.b)
        
    def from_hex(hex_color:str):
        hex_color = hex_color.replace('#','')
        match(len(hex_color)):
            case 3:
                hex_r,hex_g,hex_b = tuple(map(lambda x: int(x*2,16),hex_color))
                return RGB(hex_r,hex_g,hex_b)
            case 6:
                hex_list = unwrap(hex_color,2)
                hex_r,hex_g,hex_b = tuple(map(lambda x: int(x,16),hex_list))
                return RGB(hex_r,hex_g,hex_b)
            case _:
                print('Invalid hexadecimal value')
                
class Vec2:
    x = 0 
    y = 0
    def __init__(self):
        pass

class Grid:
    x = 0 
    y = 0 
    color_scheme = {
        0: RGB(0,0,0),
        1: RGB(255,255,255),
        2: RGB.from_hex("#0f0")
    }
    block_map = []
    blocks = None
    block_limits = None
    block_percent = None
    bots = []
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.generate_map()
        
    def render(self,screen):
        block_width = WINDOW_WIDTH // self.x
        block_height = WINDOW_HEIGHT // self.y
        for x in range(0, WINDOW_WIDTH, block_width):
            ix = math.floor(x/block_width if x > 0 else 0)
            for y in range(0, WINDOW_HEIGHT, block_height):
                iy = math.floor(y/block_height if y > 0 else 0)
                block = self.block_map[ix][iy]
                color = self.color_scheme[block].__raw__()
                yel = RGB(44,0,78).__raw__()
                color = random.choice([color,yel])
                rect = pygame.Rect(x, y, block_width, block_height)
                pygame.draw.rect(screen, color, rect, 0)
                pygame.draw.rect(screen, RGB(0,0,0).__raw__(), rect, 1)
                
    def generate_map(self):
        block_counts = {b:0 for b in BLOCKS}
        total_blocks = (self.x*self.y)-1
        assigned_blocks = 0
        available_blocks = [b for b in BLOCKS]
        for x in range(0,self.x):
            self.block_map.append([])
            y = 0
            while y < self.y:
                extra = list(filter(lambda x:BLOCKS[x] in ['empty'],available_blocks))
                opt = random.choice(available_blocks+extra)
                limit = BLOCK_LIMITS[opt] if opt in BLOCK_LIMITS else None
                ratio = BLOCK_PERCENT[opt]/100 if opt in BLOCK_PERCENT else None
                count = block_counts[opt]
                if limit is not None:
                    if count >= limit:
                        n_b = list(filter(lambda x:x != opt,available_blocks))
                        available_blocks = n_b
                        continue
                if ratio is not None:
                    if count/total_blocks >= ratio:
                        n_b = list(filter(lambda x:x != opt,available_blocks))
                        available_blocks = n_b
                        continue
                block_counts[opt] += 1
                assigned_blocks += 1
                y += 1
                self.block_map[x].append(opt)
                
    def show_map(self,d=False):
        out = ""
        for x in range(0,self.x):
            for y in range(0,self.y):
                block = self.block_map[x][y]
                out += f"{BLOCKS[block] if d else block} "
            out += "\n"
        print(out)
        
class Bot:
    position = Vec2()
    velocity = Vec2()
    max_sight = 2
    diagonal_sight:bool = False
    linear_sight:bool = True
    collision_size = 1
    discovered_map = []
    map_option = 0
    def __init__(self):
        pass
    def move_to_goal():
        pass

if __name__ == "__main__":
    start_screen(WINDOW_WIDTH,WINDOW_HEIGHT)
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    #pygame.display.set_caption("Simple Pygame Grid")
    clock = pygame.time.Clock()
    
    main_grid = Grid(10,10)
    main_grid.show_map()
    #main_bot = Bot()
    #main_grid.add_bot(main_bot)
    #main_grid.render(None)
    
    color = RGB.from_hex("#3456ef")
    #print(color)

    running = True
    
    while running:
        if keyboard.active('ctrl'):
            sys.exit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
        screen.fill(RGB(0,0,0).__raw__())
        main_grid.render(screen) 
        #main_grid.render(22) 
        
        pygame.display.flip() # Update the display
        update_screen(screen)
        clock.tick(30)
        
    pygame.quit()
    sys.exit()