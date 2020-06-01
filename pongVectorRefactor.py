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
ballspeed = 6

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
        self.vel=vec(random.randint(-5,5),random.randint(-5,5))
        self.acceleration = vec(random.randint(-5,5),random.randint(-5,5))
        self.rect.center = self.position
    def update(self, pressed_keys):
        self.acceleration = vec(0,0)
        self.vel = vec (0,0)
        #if pressed_keys[K_UP]:
            #self.acceleration.y = (-5)
        #if  pressed_keys[K_DOWN]:
            #self.acceleration.y = (5)
        if pressed_keys[K_LEFT]:
            self.acceleration.x = (-5)
        if pressed_keys[K_RIGHT]:
            self.acceleration.x = (5)
        self.vel += self.acceleration
        self.position += self.vel
        self.rect.center = self.position


        #keep player on the screen
        if self.rect.left<0:
            self.rect.left=0
        if self.rect.right>=screen_w:
            self.rect.right=screen_w
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
        self.acceleration = vec(0,0)
        self.rect.center = self.position

    def update(self, pressed_keys):
        self.acceleration = vec(0,0)
        self.vel = vec (0,0)
        #if pressed_keys[K_UP]:
            #self.acceleration.y = (-5)
        #if  pressed_keys[K_DOWN]:
            #self.acceleration.y = (5)
        if pressed_keys[K_LEFT]:
            self.acceleration.x = (-5)
        if pressed_keys[K_RIGHT]:
            self.acceleration.x = (5)
        self.vel += self.acceleration
        self.position += self.vel
        self.rect.center = self.position


        #keep player on the screen
        if self.rect.left<0:
            self.rect.left=0
        if self.rect.right>=screen_w:
            self.rect.right=screen_w
        if self.rect.top<=400:
            self.rect.top=400
        if self.rect.bottom >=screen_h:
            self.rect.bottom =screen_h
        #if self.rect.top <= ball.bot:
            #self.rect.top = ball.bot -1

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__()
        self.surf = pygame.Surface((15,15))
        self.xc = random.randint(300,450)
        self.yc = random.randint(300,450)
        self.center = (self.xc,self.yc)
        self.vel=vec(0,0)
        self.acceleration = vec(0,14)
    def update(self):
        self.edge = []
        for i in range(360):
            angle = math.radians(i)
            self.x = int(self.center[0] + radius * math.cos(angle))
            self.y = int(self.center[1] + radius * math.sin(angle))
            point = vec(self.x,self.y)
            if enemy.rect.collidepoint(point) == True:
                self.acceleration.reflect_ip(self.acceleration)
                self.acceleration=self.acceleration+enemy.acceleration
            if player.rect.collidepoint(point) == True:
                self.acceleration.reflect_ip(self.acceleration)
                self.acceleration=self.acceleration+player.acceleration
        self.vel += self.acceleration
        self.vel.scale_to_length(ballspeed)
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
