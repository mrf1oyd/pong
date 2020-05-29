#import the game module
import pygame
import random
from pygame.locals import *
import numpy

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
ballspeed = 1

vec = pygame.math.Vector2

#define a player object
#surface is now an attribute of player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((player_width,player_height))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect()
        self.rect =self.rect.move(400,800)
        self.topedge = set()
    def update(self, pressed_keys):
        self.topedge.clear()
        if pressed_keys[K_UP]:
            self.rect.move_ip(0,-5)
        if  pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)





        #keep player on the screen
        if self.rect.left<0:
            self.rect.left=0
        if self.rect.right>=screen_w:
            self.rect.right=screen_w
        if self.rect.top<=400:
            self.rect.top=400
        if self.rect.bottom >=screen_h:
            self.rect.bottom =screen_h

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((75,25))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect()
        self.rect =self.rect.move(400,0)
        self.topedge=[]
    def update(self, pressed_keys):
        self.topedge.clear()
        if pressed_keys[K_UP]:
            self.rect.move_ip(0,-5)
        if  pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

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
        self.x = random.randint(300,450)
        self.y = random.randint(300,450)
        self.center = vec(self.x,self.y)
        self.top = (self.center + vec(0,14))
        self.bot = (self.center - vec(0,14))
        self.vel=vec(0,0)
        self.acceleration = vec(0,14)
    def update(self):
        self.top = (self.center + vec(0,14))
        self.bot = (self.center - vec(0,14))
        self.vel += self.acceleration
        self.vel.scale_to_length(ballspeed)
        self.center += self.vel
        self.top = (self.center + vec(0,14))
        self.bot = (self.center - vec(0,14))
        if enemy.rect.collidepoint(ball.bot) == True:
            self.acceleration=self.acceleration.reflect(self.acceleration)
        if player.rect.collidepoint(ball.top) == True:
            self.acceleration=self.acceleration.reflect(self.acceleration)


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

while running:

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
    '''if enemy.rect.collidepoint(ball.bot) == True:
        ball.physics_sim()
    if player.rect.collidepoint(ball.top) == True:
        ball.physics_sim()'''
    ball.update()
    #get key pressed
    pressed_keys=pygame.key.get_pressed()
    #update player sprite with info on key pressed
    player.update(pressed_keys)
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
