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

#defines a player object
#surface is now an attribute of player
class Text():
    def __init__(self, text, size, font_color, background_color=None):
        self.font = pygame.font.Font(None, size)
        self.surf = self.font.render(text, True, font_color, background_color)
        self.rect = self.surf.get_rect()
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((player_width,player_height))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect()
        self.rect = self.rect.move(400,800)
        self.rect.center=vec(self.rect.center)
        self.vel=vec(0,0)
    def update(self, pressed_keys):
        if pressed_keys[K_LEFT]:
            self.vel.x = (-playerspeed)
        if pressed_keys[K_RIGHT]:
            self.vel.x = (playerspeed)
        self.rect.center += self.vel
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

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf=pygame.Surface((75,25))
        self.surf.fill((255,255,255))
        self.rect=self.surf.get_rect()
        self.rect=self.rect.move(400,0)
        self.rect.center=vec(self.rect.center)
        self.vel=vec(0,0)

    def update(self, ball):
        #kindof a predictive algorithm. def a first pass.
        ball.copycenter=ball.center
        if random.randint(0,100) >= 25:
            if ball.center.y >=30 and ball.vel.y > 0:
                if (self.rect.centerx+100) > ball.copycenter.x+200 and ball.vel.x < 0:
                    self.vel.x = (-5)
                if (self.rect.centerx-100) < ball.copycenter.x-200 and ball.vel.x >0:
                    self.vel.x = (5)
            if ball.center.y <= 760 and ball.vel.y < 0:
                if self.rect.centerx > ball.copycenter.x+50 and ball.vel.x < 0:
                    self.vel.x = (-5)
                if self.rect.centerx < ball.copycenter.x-50 and ball.vel.x > 0:
                    self.vel.x = (5)
        self.rect.center += self.vel
        self.vel=vec(0,0)
        #keep enemy on the screen
        if self.rect.left<=0:
            self.rect.left=0
        if self.rect.right>=screen_w:
            self.rect.right=screen_w
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__()
        self.surf = pygame.Surface((15,15))
        self.xc = random.randint(300,450)
        self.yc = random.randint(300,450)
        self.center = vec(self.xc,self.yc)
        self.vel=vec(random.randint(1,3),random.randint(1,5))
        self.exists = True

    def update(self):
        self.edge = []
        for i in range(360):
            angle = math.radians(i)
            self.x = int(self.center[0] + radius * math.cos(angle))
            self.y = int(self.center[1] + radius * math.sin(angle))
            point = (self.x,self.y)
            #if ball collides with bounds on the right a reflection vector is generated.
            if self.x >= 800:
                self.vel.x=self.vel.x * (-1)
                self.vel.y=self.vel.y * (1)
            #if ball collides with bounds on the left a refelection vector is generated
            if self.x <= 0:
                self.vel.x=self.vel.x * (-1)
                self.vel.y=self.vel.y * (1)
            #if enemy collides with ball a reflection vector is generated
            if enemy.rect.collidepoint(point) == True:
                self.vel.x=self.vel.x * (1)+.01
                self.vel.y=self.vel.y * (-1)-.01
            #if player collides with ball a reflection vector is generated
            if player.rect.collidepoint(point) == True:
                self.vel.x=self.vel.x * (1)+.01
                self.vel.y=self.vel.y * (-1)-.01
            #kills sprite if beyond top and bottom bounds
            if self.y >= 800 or self.y<=0:
                self.kill()
        self.center += self.vel
#initalize game
pygame.init()
#initialize the font module
pygame.font.init()
#create screen object
screen = pygame.display.set_mode([screen_w,screen_h])
#instantiate player 1
player = Player()
#instantiate the enemy
enemy = Enemy()
#instantiate the ball
ball = Ball()
#variable keeping game runing
running = False
ballinplay = True
radius = 10
title = Text('PONG', 200, (255,255,255))
title.rect.center = (400,200)
instructions = Text('press enter to play', 25, (255,255,255))
instructions.rect.center = (400,600)
goalmessage = Text('GOAL!!', 200, (255,255,255))
goalmessage.rect.center = (400,400)

while running != True:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                running = True
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            pygame.quit()
    screen.fill((0,0,0))
    screen.blit(title.surf, title.rect)
    screen.blit(instructions.surf, instructions.rect)
    #update display
    pygame.display.flip()

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
        screen.blit(goalmessage.surf, goalmessage.rect)
        pygame.display.update()
        pygame.time.wait(300)
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
