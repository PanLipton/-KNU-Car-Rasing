import pygame #imort pygame module
from sys import exit #imort sys module
import sys
import os
from pygame.locals import *
import math  # Import the math module
from pygame.math import Vector2


class AActor(pygame.sprite.Sprite):
    screen=None
    _x=0
    _y=0
    _w=0
    _h=0
    _rect = pygame.Rect(0,0,0,0)
    def __init__(self,screen,image,x,y,w,h):
        super().__init__()
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self.image = image
        self.image = pygame.transform.scale(image,(w,h))
        self.screen = screen
        self._rect = pygame.Rect(x,y,w,h)
        self.FRotator = 90
    def draw(self):
        # Calculate the rotation angle based on the FRotator
        angle = self.FRotator
        rotated_image = pygame.transform.rotate(self.image, angle-90)
        self.rect = self.image.get_rect(center=(self._x,self._y))
        # Blit the rotated image using the new center position
        self.screen.blit(rotated_image, self.rect.center)

    def getActorLocation(self)->Vector2:
        return Vector2(self._x,self._y)
    def setActorLocation(self,Location:Vector2):
        self._x = Location[0]
        self._y = Location[1]


"""
#test AActor game loop

#init game
pygame.init()

#initialize screen object
screen = pygame.display.set_mode((1000,1000))
actor = AActor(screen,"pink-car.png",0,0,50,100)
clock = pygame.time.Clock()
#Title
pygame.display.set_caption("Car Racing")

dist =1;
#Game Loop
while True:
    #handling events
    for event in pygame.event.get():
        #crossarrow button pressed
        if(event.type == pygame.QUIT):
            #quit game
            pygame.quit()
            exit()
        keys = pygame.key.get_pressed()
        move_x = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        move_y = keys[pygame.K_DOWN] - keys[pygame.K_UP]
        actor.setActorLocation((move_x * 5, move_y * 5))
    # Get the mouse position as the target point
    target_point = Vector2(pygame.mouse.get_pos())

    # Set player rotation based on the target point
    #print(actor.FindLookAtRotation(actor.getActorLocation(), target_point))
    actor.setActorRotation(-actor.FindLookAtRotation(actor.getActorLocation(), target_point))
    
    screen.fill([255, 255, 255])
    actor.draw()
    #update screen
    pygame.display.update()
    clock.tick(60)
"""
