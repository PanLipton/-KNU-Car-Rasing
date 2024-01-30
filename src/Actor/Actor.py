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
    def getActorRotation(self) -> float:
        return self.FRotator

    def setActorRotation(self, angle: float):
        self.FRotator = angle

    def FindLookAtRotation(self, start: Vector2, end: Vector2) -> float:
        # Calculate the rotation angle in degrees
        direction_vector = end - start
        return math.degrees(math.atan2(direction_vector.y, direction_vector.x))