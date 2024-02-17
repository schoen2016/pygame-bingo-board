from math import floor, ceil
import pygame
class WINDOW():
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def pos(self):
        return (self.x, self.y)
    
    def size(self):
        return (self.width, self.height)

# SCREEN_WIDTH = 800
# SCREEN_HEIGHT = 600
# GUI = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
GUI = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
SCREEN_WIDTH = pygame.display.Info().current_w
SCREEN_HEIGHT = pygame.display.Info().current_h
WIN_MAIN = WINDOW(
    x = 0,
    y = 0,
    width = SCREEN_WIDTH,
    height = SCREEN_HEIGHT
)
WIN_LEFT = WINDOW(
    x = 0,
    y = floor(SCREEN_HEIGHT * .50),
    width = ceil(SCREEN_WIDTH * .30),
    height = ceil(SCREEN_HEIGHT * .50)
)
WIN_MID = WINDOW(
    x = floor(SCREEN_WIDTH * .30), 
    y = floor(SCREEN_HEIGHT * .50),
    width = ceil(SCREEN_WIDTH * .30),
    height = ceil(SCREEN_HEIGHT * .50)
)
WIN_RIGHT = WINDOW(
    x = floor(SCREEN_WIDTH * .60), 
    y = floor(SCREEN_HEIGHT * .50),
    width = ceil(SCREEN_WIDTH * .40),
    height = ceil(SCREEN_HEIGHT * .50)
)


pygame.display.set_caption("Bingo Board")