import os
from math import floor
import pygame
from colors import color_gray, color_white, color_black, color_red

class Ball(pygame.sprite.Sprite):
    def __init__(self, text, coordinates:tuple, size:tuple):
        pygame.sprite.Sprite.__init__(self)
        self.image = self.get_image(text)
        self.fonttype = 'Comic Sans MS'
        self.rect = self.image.get_rect()
        self.rect.x = coordinates[0]
        self.rect.y = coordinates[1]
        self.text = text
        self.hidden = True
        self.fontcolor = color_black
        self.fontsize = floor(size[0]/2)
        self.coordinates = coordinates
        self.surface = None
        self.size = size
        self._label()

    def get_image(self, text):
        sprite = pygame.image.load(os.path.join('src/Bingo Balls All 200 px.png')).convert_alpha()
        
        blue = ["B",'-']
        blue.extend([str(i) for i in range(0,16)])

        yellow = ["I"]
        yellow.extend([str(i) for i in range(16,31)])

        green = ["N"]
        green.extend([str(i) for i in range(31,46)])
        
        black = ["G"]
        black.extend([str(i) for i in range(46,61)])
        
        red = ["O"]
        red.extend([str(i) for i in range(61,76)])
        
        index = None
        colors = [blue,yellow,green,black,red]

        for i, color in enumerate(colors):
            if text in color:
                index = i

        image = pygame.Surface([200,200])
        width = 200
        height = 200
        left = index * width
        top = 0
        
        image = pygame.Surface([width,height])
        image.blit(sprite, (0,0), (left,top,width,height))
        image.set_colorkey((0,0,0))
        return image

    def _label(self):
        self.resize(self.size)

        # Create ball text
        font = pygame.font.SysFont(self.fonttype, self.fontsize)
        textsurface = font.render(self.text, True, self.fontcolor)
        fx, fy = textsurface.get_size()
        fx = self.size[0]/2-fx/2
        fy = self.size[1]/2-fy/2

        # Add font to ball
        self.image.blit(textsurface, (fx,fy))
    
    def frame_action(self):
        size = self.size
        self.resize(size)
        if self.mouse_over():
            size = (size[0]*.5, size[1]*.5)
            self.resize(size)
    
    def get(self):
        return self.surface
    
    def coordinates(self):
        return self.coordinates

    def set_coordinates(self, coordinates:tuple):
        self.rect.x = coordinates[0]
        self.rect.y = coordinates[1]       
    
    def resize(self, size):
        self.image = pygame.transform.scale(self.image, size)
        coordinate = (self.rect.x, self.rect.y)
        self.rect = self.image.get_rect()
        self.rect.x = coordinate[0]
        self.rect.y = coordinate[1]
    
    def mouse_over(self):
        point = pygame.mouse.get_pos()
        return self.rect.collidepoint(point)
