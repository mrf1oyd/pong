#import the game module
import pygame
import random
from pygame.locals import *
import math

#import pygame.locals for easy key coordinate access
from pygame.locals import (
        K_UP,
        K_DOWN,
        K_LEFT,
        K_RIGHT,
        K_ESCAPE,
        KEYDOWN,
        QUIT,)
#define screen constants
screen_w=800
screen_h=800
#define player constants
player_width = 75
player_height = 25
playerspeed = 5

vec = pygame.math.Vector2

#define a player object
#surface is now an attribute of player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((player_width,player_height))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect()
        self.rect = self.rect.move(400,800)
        self.position=vec(self.rect.center)
        self.vel= vec(0,0)
        self.rect.center = self.position
    def update(self, pressed_keys):
        #if pressed_keys[K_UP]:
            #self.acceleration.y = (-5)
        #if  pressed_keys[K_DOWN]:
            #self.acceleration.y = (5)
        if pressed_keys[K_LEFT]:
            self.vel.x = (-playerspeed)
        if pressed_keys[K_RIGHT]:
            self.vel.x = (playerspeed)
        self.position += self.vel
        self.rect.center = self.position
        self.vel=vec(0,0)

        #keep player on the screen
        if self.rect.left<0:
            self.rect.left=0
            self.vel=vec(0,0)
        if self.rect.right>=screen_w:
            self.rect.right=screen_w
            self.vel=vec(0,0)
        if self.rect.top<=400:
            self.rect.top=400
        if self.rect.bottom >=screen_h:
            self.rect.bottom =screen_h
        #if self.rect.top <= ball.bot:
            #self.rect.top = ball.bot -1

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((75,25))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect()
        self.rect =self.rect.move(400,0)
        self.position=vec(self.rect.center)
        self.vel=vec(0,0)
        self.rect.center = self.position
    def update(self, ball):
        #kindof a predictive algorithm. def a first pass
        #ix,iy reprepsents intersect x and y
        self.ix = ball.center.x
        self.iy = ball.center.y
        ball.copyx = ball.center.x
        ball.copyy = ball.center.y
        # help delay tracking process? iterates a copy of x and y as an attempt to solve for when the ball will cross the y axis
        if ball.center.y <= 770:
            if self.iy > 0:
                ball.copyx+=ball.vel.x
                ball.copyy+=ball.vel.y
                self.iy = ball.copyy
            self.ix=ball.copyx
        if self.position.x < self.ix:
            self.vel.x = (playerspeed)
        if self.position.x > self.ix:
            self.vel.x = (-playerspeed)
        self.position += self.vel
        self.rect.center = self.position
        self.vel=vec(0,0)

        #keep enemy on the screen
        if self.rect.left<0:
            self.rect.left=0
        if self.rect.right>=screen_w:
            self.rect.right=screen_w
        if self.rect.top<=0:
            self.rect.top=0
        if self.rect.bottom >=400:
            self.rect.bottom =400
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__()
        self.surf = pygame.Surface((15,15))
        self.xc = random.randint(300,450)
        self.yc = random.randint(300,450)
        self.center = vec(self.xc,self.yc)
        self.vel=vec(random.randint(0,3),random.randint(1,5))
        self.exists = True
    def update(self):
        self.edge = []
        for i in range(360):
            angle = math.radians(i)
            self.x = int(self.center[0] + radius * math.cos(angle))
            self.y = int(self.center[1] + radius * math.sin(angle))
            point = vec(self.x,self.y)
            #if ball collides with bounds on the right a reflection vector is generated
            if self.x == 800:
                self.vel.x=self.vel.x * (-1)
                self.vel.y=self.vel.y * (1)
            #if ball collides with bounds on the left a refelection vector is generated
            if self.x == 0:
                self.vel.x=self.vel.x * (-1)
                self.vel.y=self.vel.y * (1)
            #if enemy collides with ball a reflection vector is generated
            if enemy.rect.collidepoint(point) == True:
                self.vel.x=self.vel.x * (1)
                self.vel.y=self.vel.y * (-1)
                self.vel=self.vel+(enemy.vel*.9)
            #if player collides with ball a reflection vector is generated
            if player.rect.collidepoint(point) == True:
                self.vel.x=self.vel.x * (1)
                self.vel.y=self.vel.y * (-1)
                self.vel=self.vel+(player.vel*.9)
            #kills sprite if beyond top and bottom bounds
            if self.y >= 800 or self.y<=0:
                self.kill()
        self.center += self.vel



#initalize game
pygame.init()
#create screen object
screen = pygame.display.set_mode([screen_w,screen_h])
#instantiate player 1
player = Player()
#instantiate the enemy
enemy = Enemy()
#instantiate the ball
ball = Ball()
#variable keeping game runing
running = True
ballinplay = True
radius = 10

#initialize the bounds
boundsL=[]
boundsR=[]
for i in range(screen_h):
    bounds_point = (0, i)
    boundsL.append(bounds_point)
for i in range(screen_h):
    bounds_point = (screen_w, i)
    boundsR.append(bounds_point)

while running:

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
    #checks if ball exists if not instantiates a new one
    if ball.center.y <= 0 or ball.center.y >= 800:
        ball.kill()
        pygame.display.update()
        pygame.time.wait(250)
        ball = Ball()
    ball.update()
    #get key pressed
    pressed_keys=pygame.key.get_pressed()
    #update player sprite with info on key pressed
    player.update(pressed_keys)
    #update the enemy sprite with info from game
    enemy.update(ball)
    #fill screen
    screen.fill((0,0,0))
    #draw player
    screen.blit(player.surf, player.rect)
    #draw the enemy
    screen.blit(enemy.surf, enemy.rect)
    #draw the ball
    pygame.draw.circle(screen, (255,255,255), (ball.center), (radius))
    #update display
    pygame.display.flip()
