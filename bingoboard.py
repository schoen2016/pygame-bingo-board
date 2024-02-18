import pygame
import sys
import random
import subprocess
import math
from pygame.locals import *
import os
from math import floor,ceil
from display import WIN_LEFT, WIN_MAIN, WIN_RIGHT, WIN_MID
from display import WINDOW, GUI
from ball import Ball
from colors import color_gray, color_white, color_black, color_red

run = True
pad = 5     # padding between balls
br = ceil(WIN_MAIN.width/(17*2+pad))  # ball radius
bw = 2*br   # ball width
bh = 2*br   # ball height
fs = br     # ball font size
background_color = color_gray
GUI.fill(background_color)

      
class Img():
    def __init__(self):
        self.fonttype = 'Comic Sans MS'

class Badge(pygame.sprite.Sprite):
    def __init__(self, image:pygame.Surface, pos, 
                 deactivate_alpha = 25):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.size = image.get_size()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.text = ''
        self.deactive_alpha = deactivate_alpha
        self.active = False
        self.deactivate()
    
    def resize(self, size):
        self.image = pygame.transform.scale(self.image, size)
        pos = (self.rect.x, self.rect.y)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.size = size

    def deactivate(self):
        self.image.set_alpha(self.deactive_alpha)
        self.active = False
    
    def activate(self):
        self.image.set_alpha(255)
        self.active = True
    
    def toggle(self):
        if self.active:
            self.deactivate()
        else:
            self.activate()

    def set_text(self, text, fonttype, fontsize, fontcolor):
        # Create ball text
        self.text = text
        font = pygame.font.SysFont(fonttype, fontsize)
        textsurface = font.render(text, True, fontcolor)
        tw, th = textsurface.get_size()
        tw = self.size[0]/2-tw/2
        th = self.size[1]/2-th/2

        # Add font to ball
        self.image.blit(textsurface, (tw,th))

class TextBlock(pygame.sprite.Sprite):
    def __init__(self, surf:pygame.Surface):
        pygame.sprite.Sprite.__init__(self)
        self.image = surf
        self.rect = self.image.get_rect()
    
    def set_pos(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        
def board_position(
        num:int,    # ball number
        radius:int, # ball radius
        padding:int # padding between balls
) -> tuple:
    if num < 15:
        i = num
        yPos = 20
        
    if num >= 15 and num < 30:
        i = num - 15
        yPos = 20 + ( radius*2  + padding ) * 1

    if num >= 30 and num < 45:
        i = num - 30
        yPos = 20 + ( radius*2 + padding ) * 2 

    if num >= 45 and num < 60:
        i = num - 45
        yPos = 20 + ( radius*2 + padding ) * 3
        
    if num >= 60 and num < 75:
        i = num - 60
        yPos = 20 + ( radius*2 + padding ) * 4

    xPos = (2*radius+padding)*i + radius*2 + radius
    return (xPos,yPos)

def menu_position(
        num:int,    # ball number
        radius:int, # ball radius
        padding:int # padding between balls
) -> tuple:
    xPos = 0
    yPos = 0
    SUBTILE = WINDOW(
        x = WIN_LEFT.x + floor(radius*1.5),
        y = WIN_LEFT.y,
        width = WIN_LEFT.width - ceil(radius*1.5),
        height = WIN_LEFT.height
    )
    
    width =  radius*2 + (radius*2 + padding) * 2
    height = radius*2 + (radius*2 + padding) * 4
    BTILE = WINDOW(
        x = WIN_LEFT.x + floor((SUBTILE.width - width)/2),
        y = WIN_LEFT.y + floor((SUBTILE.height - height)/2),
        width = width,
        height = height
    )
    
    # menu balls x positions
    if num % 3 == 1:
        xPos = BTILE.x + (radius*2 + padding) * 1
    elif num % 3 == 2:
        xPos = BTILE.x + (radius*2 + padding) * 2
    elif num % 3 == 0:
        xPos = BTILE.x + (radius*2 + padding) * 3

    # menu balls y positions
    if num % 15 in range(1,4):
        yPos = BTILE.y
    if num % 15 in range(4,7):
        yPos = BTILE.y + (radius*2 + padding) * 1
    if num % 15 in range(7,10):
        yPos = BTILE.y + (radius*2 + padding) * 2
    if num % 15 in range(10,13):
        yPos = BTILE.y + (radius*2 + padding) * 3
    if num % 15 in range(13,15) or num % 15 == 0:
        yPos = BTILE.y + (radius*2 + padding) * 4
    
    return (xPos,yPos)

def menu_bingo_position(
        num:int,    # ball number
        radius:int, # ball radius
        padding:int # padding between balls
) -> tuple:

    xPos = 0
    yPos = 0
    
    height = radius*2 + (radius*2 + padding) * 4
    SUBTILE = WINDOW(
        x = WIN_LEFT.x,
        y = WIN_LEFT.y + floor((WIN_LEFT.height - height)/2),
        width = WIN_LEFT.width - ceil(radius*1.5),
        height = WIN_LEFT.height
    )
    xPos = SUBTILE.x + 5
    yPos = SUBTILE.y + (radius*2 + padding) * (num - 1)
    return((xPos,yPos))

def bingo_position(
        num:int,    # ball number
        radius:int, # ball radius
        padding:int # padding between balls
) -> tuple:

    xPos = 5
    yPos = 20 + ( radius*2  + padding )  * (num - 1)
    
    # xPos = (radius*2 + padding)
    # yPos = (radius*2 + padding) * (num - 1)
    return((xPos,yPos))

def create_board_balls():
    
    balls = [ Ball(str(num+1), (22,17), (bw,bh)) for num in range(0,75) ]
    for i, ball in enumerate(balls):
        radius = floor(ball.image.get_size()[0]/2)
        coordinates = board_position(i, radius, pad)
        ball.set_coordinates(coordinates)

    return balls

def create_menu_sprite_groups():
    '''
        Returns a list of sprite groups associated with a Bingo letter.
        B: 1-15
        I: 16-30
        N: 31-45
        G: 46-60
        O: 61-75 
    '''
    balls = [ Ball(str(num+1), (0,0), (bw,bh)) for num in range(0,75) ]
    groups = list()
    group = pygame.sprite.Group()
    for i, ball in enumerate(balls):

        radius = floor(ball.image.get_size()[0]/2)
        coordinates = menu_position(i+1, radius, pad)
        ball.set_coordinates(coordinates)
            
        group.add(ball)
        if (i+1) % 15 == 0:
            groups.append(group)
            group = pygame.sprite.Group()

    groups.append(group)
    return {
        "B": groups[0],
        "I": groups[1],
        "N": groups[2],
        "G": groups[3],
        "O": groups[4],
    }

def create_bingo():
    balls = []
    balls.append(Ball('B', (0,0), (bw,bh)))
    balls.append(Ball('I', (0,0), (bw,bh)))
    balls.append(Ball('N', (0,0), (bw,bh)))
    balls.append(Ball('G', (0,0), (bw,bh)))
    balls.append(Ball('O', (0,0), (bw,bh)))
    for i, ball in enumerate(balls):
        radius = floor(ball.image.get_size()[0]/2)
        coordinates = bingo_position(i+1, radius, pad)
        ball.set_coordinates(coordinates)
        all_sprites.add(ball)

    return {
        "B": balls[0],
        "I": balls[1],
        "N": balls[2],
        "G": balls[3],
        "O": balls[4],
    }

def create_menu_bingo():
    balls = []
    balls.append(Ball('B', (0,0), (bw,bh)))
    balls.append(Ball('I', (0,0), (bw,bh)))
    balls.append(Ball('N', (0,0), (bw,bh)))
    balls.append(Ball('G', (0,0), (bw,bh)))
    balls.append(Ball('O', (0,0), (bw,bh)))
    for i, ball in enumerate(balls):
        radius = floor(ball.image.get_size()[0]/2)
        coordinates = menu_bingo_position(i+1, radius, pad)
        ball.set_coordinates(coordinates)
        all_sprites.add(ball)

    return {
        "B": balls[0],
        "I": balls[1],
        "N": balls[2],
        "G": balls[3],
        "O": balls[4],
    }

def set_menu_group(balls:dict, current):
    point = pygame.mouse.get_pos()
    for letter, ball in balls.items():
        if ball.rect.collidepoint(point):
            return letter
    return current

def letter_index(letter:str):
    if letter == "B":
        return 0
    elif letter == "I":
        return 1
    elif letter == "N":
        return 2
    elif letter == "G":
        return 3
    elif letter == "O":
        return 4
    else:
        raise KeyError("letter must be B,I,N,G,O")

def update_ball(balls, index):
    '''
        Removes or adds ball from sprite group
    '''
    for ball in balls:
        is_num = ball.text == str(index+1)
        is_hidden = ball.hidden == True

        # draw ball
        if is_num and is_hidden:
            all_sprites.add(balls[BI-1])
            balls[BI-1].hidden = False
        
        # remove ball
        if is_num and not is_hidden:
            for ball in balls:
                if ball.text == str(index+1):
                    ball.hidden = True
                    ball.kill()

def create_stage(str1,str2):
    # number ball
    # sizeN = (br*2*4, br*2*4)
    width = floor(WIN_RIGHT.width * .70)
    left = WIN_RIGHT.x + floor((WIN_RIGHT.x - width)/2)
    top = WIN_RIGHT.y + floor((WIN_RIGHT.y - width)/2)
    bw = floor(width * .90)
    bh = bw
    sw = floor(width * .60)
    sh = sw
    
    sx = left
    sy = top
    bx = floor((WIN_RIGHT.width - width))
    by = floor((WIN_RIGHT.height - width))

    bx = WIN_RIGHT.x + WIN_RIGHT.width - bw
    by = WIN_RIGHT.y + WIN_RIGHT.height - bw
    sx = bx - floor(sw/2)
    sy = by - floor(sh/2)

    sx = WIN_RIGHT.x + floor((WIN_RIGHT.width - (bw + floor(sw/2)))/2)
    sy = WIN_RIGHT.y + floor((WIN_RIGHT.height - (bh + floor(sh/2)))/2)
    bx = sx + floor(sw/2)
    by = sy + floor(sh/2)

    ballN = Ball(str1, (bx,by), (bw,bw))
    ballL = Ball(str2, (sx,sy), (sw,sw))

    return ballN, ballL

def badge_position(index2D:tuple, size:tuple):
    xPos = 0
    yPos = 0
    
    width = size[0]*3 + pad*2
    height = size[1]*4 + (br+5)*3
    print(
        "br: {} height {} WIN_MID.height {}"
        .format(br, height,WIN_MID.height)
    )
    SUBTILE = WINDOW(
        x = WIN_MID.x + floor((WIN_MID.width - width)/2),
        y = WIN_MID.y + floor((WIN_MID.height - height)/2) + 10,
        width = width,
        height = height
    )
    xpad = pad * index2D[0] if index2D[0] != 0 else 0
    ypad = (br+5) * index2D[1] if index2D[1] != 0 else 0
    xPos = SUBTILE.x + size[0] * index2D[0] + xpad
    yPos = SUBTILE.y + size[1] * index2D[1] + ypad
    return (xPos, yPos)

def create_badges():
    badges = list()
    text = ['\u00A7', '\u221E', '\u20AC', '\u20AC']
    for i in range(0,3):
        for j in range(0,4):
            pos = badge_position((i,j), (br*2,br*2))
            ball = get_ball('red')

            badge = Badge(ball, pos)

            badge.resize((br*2,br*2))
            badge.set_text(
                text = text[j],
                fonttype = 'Comic Sans MS',
                fontsize = br,
                fontcolor = color_black
            )
            
            # badge.image.set_alpha(255/2)
            badges.append(badge)
    
    return badges

def create_badge_titles(badges):
    # Badge Titles
    fonttype = 'Comic Sans MS'
    fontcolor = color_white
    fontsize = br
    titles = [
        'Cover All',
        'Postage Stamp',
        'Corners',
        'Bingo',
    ]
    pos = list()
    blocks = list()
    for i in range(0,len(badges),3):
        x = badges[i].rect.x
        y = badges[i].rect.y
        pos.append((x,y))
        print(i)
        print(badges[i].text)

    for text, pos in zip(titles, pos):
        font = pygame.font.SysFont(fonttype, fontsize)
        textsurface = font.render(text, True, fontcolor)
    
        block = TextBlock(textsurface)
        xPos = pos[0]
        yPos = pos[1] - fontsize - 5
        block.set_pos((xPos,yPos))
        blocks.append(block)
    return blocks

    # tw, th = textsurface.get_size()
    # fx = self.size[0]/2-fx/2
    # fy = self.size[1]/2-fy/2

    # Add font to ball
    # self.image.blit(textsurface, (fx,fy))

def get_bingo(color:str, image):
    sprite = pygame.Surface([200,200])
    left = 0
    top = 0
    width = 200
    height = 200
    
    sprite = pygame.Surface([width,height])
    sprite.blit(image, (0,0), (left,top,width,height))
    sprite.set_colorkey((0,0,0))
    return sprite

def get_frame(surface, rect):
        
    left = rect[0]
    top = rect[1]
    width = rect[2] 
    height = rect[3]
    
    image = pygame.Surface([rect[2],rect[3]])
    image.blit(surface, (0,0), (left,top,width,height))
    # image.set_colorkey((0,0,0))
    return image

def get_ball(color:str):
    
    index = None
    if color == 'blue':
        index = 0
    elif color == 'yellow':
        index = 1
    elif color == 'green':
        index = 2
    elif color == 'black':
        index = 3
    elif color == 'red':
        index = 4
    else:
        index = 0
    
    sprite = pygame.image.load(os.path.join('Bingo Balls All 200 px.png')).convert_alpha()
    rect = [index * 200, 0, 200, 200]

    return get_frame(sprite,rect)

def draw_grid(surface, blocksize, thickness):
    bs = blocksize
    for x in range(0,5):
        for y in range(0,5):
            pygame.draw.rect(surface,color_white,[x*bs,y*bs,bs,bs],thickness)

def draw_badge_1(size, thickness):
    s = size
    blocksize = floor(s/5)
    b = blocksize
    surface = pygame.surface.Surface([s,s])
    pygame.draw.rect(surface,color_red,[3*b, 0, b, b])
    pygame.draw.rect(surface,color_red,[4*b, 0, b, b])
    pygame.draw.rect(surface,color_red,[3*b, 1*b, b, b])
    pygame.draw.rect(surface,color_red,[4*b, 1*b, b, b])
    draw_grid(surface, blocksize, thickness)
    
    return surface

def draw_badge_2(size, thickness):
    s = size
    blocksize = floor(s/5)
    b = blocksize
    surface = pygame.surface.Surface([s,s])
    pygame.draw.rect(surface,color_red,[0, 1*b, b, b])
    pygame.draw.rect(surface,color_red,[1*b, 1*b, b, b])
    pygame.draw.rect(surface,color_red,[2*b, 1*b, b, b])
    pygame.draw.rect(surface,color_red,[3*b, 1*b, b, b])
    pygame.draw.rect(surface,color_red,[4*b, 1*b, b, b])
    draw_grid(surface, blocksize, thickness)
    
    return surface

def draw_badge_3(size, thickness):
    s = size
    blocksize = floor(s/5)
    b = blocksize
    surface = pygame.surface.Surface([s,s])
    pygame.draw.rect(surface,color_red,[0, 0, b, b])
    pygame.draw.rect(surface,color_red,[4*b, 0, b, b])
    pygame.draw.rect(surface,color_red,[0, 4*b, b, b])
    pygame.draw.rect(surface,color_red,[4*b, 4*b, b, b])
    draw_grid(surface, blocksize, thickness)
    
    return surface

def draw_badge_4(size, thickness):
    s = size
    blocksize = floor(s/5)
    b = blocksize
    surface = pygame.surface.Surface([s,s])
    pygame.draw.rect(surface,color_red,[0, 0, s, s])
    draw_grid(surface, blocksize, thickness)
    
    return surface

def create_badges():
    ''' badges are the squares in the board area.
    '''
    padX = 10
    padY = 10
    n = 3 #num_badges
    m = 4 # num of badge sets
    
    # badge width
    bw = floor((WIN_MID.height - (m+1)*padX)/m)
    
    width = (n+1)*padX + n*bw
    height = (m+1)*padY + m*bw
    
    SUBTILE = WINDOW(
        x = WIN_MID.x + floor((WIN_MID.width - width)/2),
        y = WIN_MID.y + floor((WIN_MID.height - height)/2),
        width = width,
        height = height
    )
    badges = pygame.sprite.Group()

    # Postage Stamp
    for i in range(0,n):
        pos = (SUBTILE.x + bw*i + padX*(i+1), SUBTILE.y+padY)
        badge = Badge(draw_badge_1(100, 4),pos)
        badge.resize((bw,bw))
        badges.add(badge)

    # Bingo
    for i in range(0,n):
        pos = (SUBTILE.x + bw*i + padX*(i+1), SUBTILE.y + bw*1+padY*2)
        badge = Badge(draw_badge_2(100,4),pos)
        badge.resize((bw,bw))
        badges.add(badge)

    # Corners
    for i in range(0,n):
        pos = (SUBTILE.x + bw*i + padX*(i+1), SUBTILE.y + bw*2+padY*3)
        badge = Badge(draw_badge_3(100,4),pos)
        badge.resize((bw,bw))
        badges.add(badge)

    # Cover All
    for i in range(0,n):
        pos = (SUBTILE.x + bw*i + padX*(i+1), SUBTILE.y + bw*3+padY*4)
        badge = Badge(draw_badge_4(100,4),pos)
        badge.resize((bw,bw))
        badges.add(badge)
    return badges
    


pygame.init()
all_sprites = pygame.sprite.Group()
ball_sprites = pygame.sprite.Group()

balls = create_board_balls()
menu = create_menu_sprite_groups()
menu_balls = create_menu_bingo()
bingo_balls = create_bingo()
badges = create_badges()

for badge in badges:
    all_sprites.add(badge)


badge = get_ball('red') 

# badge = Badge(badge,(0,0))
# print(badge)

# badge = Badge(sprite,(0,0))
# print(badge)
# all_sprites.add(badge)

# all_sprites.add(badge_titles)

# all_sprites.add(ColorBall('blue',None,None,None))
# all_sprites.add(ColorBall('red',None,None,None))
# all_sprites.add(ColorBall('yellow',None,None,None))
letter = 'B'
BI = None
number_stage, letter_stage = create_stage('-','-')

clock = pygame.time.Clock()
fps = 120
while run:
    GUI.fill((20, 20, 20))
    dt = clock.tick(fps)
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run =False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                run = False
        if event.type == pygame.MOUSEBUTTONUP:

            # check menu for updates
            for i, item in enumerate(menu[letter].sprites()):
                point = pygame.mouse.get_pos()
                if item.rect.collidepoint(point):

                    # row number on status board
                    LI = letter_index(letter)
                    # calculate index of the ball to display
                    BI = (LI * 15) + i + 1

                    # update sprite list to draw
                    update_ball(balls, BI-1)

                    # Draw Large Select Ball
                    number_stage.kill()
                    letter_stage.kill()
                    number_stage, letter_stage = create_stage(str(BI), letter)
                    all_sprites.add(number_stage)
                    all_sprites.add(letter_stage)
                
            for i, item in enumerate(badges.sprites()):
                point = pygame.mouse.get_pos()
                if item.rect.collidepoint(point):
                    item.toggle()

    # print(br*2)
    surf = pygame.surface.Surface([WIN_MID.width, WIN_MID.height])
    # pygame.draw.rect(surf,color_white,[
    #     WIN_LEFT.x,WIN_LEFT.y,WIN_LEFT.width,WIN_LEFT.height
    # ])

    
    # sprite = pygame.image.load(os.path.join('Bingo Balls All 200 px.png'))
    # image = pygame.Surface([200,200])
    # image.blit(sprite, (0,0), (0,0,200,200))
    # image.set_colorkey((0,0,0))
    # badge = get_ball('red') 
    # print(image)
    # print(sprite)
    # GUI.blit(image,(0,0))
    # GUI.blit(sprite,(0,200))
    # GUI.blit(badge,(0,400))
    # GUI.blit(surf, (WIN_MID.x,WIN_MID.y))
    # badge1 = Badge(draw_badge_1(), (floor(WIN_MAIN.width/2),100))
    # all_sprites.add(badge1)

    # for ball in balls:
    #     ball_sprites.add(ball)

    ball_sprites.update()
    ball_sprites.draw(GUI)
    all_sprites.update()
    all_sprites.draw(GUI)
    badges.update()
    badges.draw(GUI)

    letter = set_menu_group(menu_balls, letter)
    menu[letter].update()
    menu[letter].draw(GUI)

    pygame.display.update()
    pygame.display.flip()

pygame.quit()
