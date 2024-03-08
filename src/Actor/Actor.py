import pygame  # imort pygame module
from sys import exit  # imort sys module
import sys
import os
from pygame.locals import *
import math  # Import the math module
from pygame.math import Vector2

sys.path.append("../Collision")

from Collision.Collision import *


class AActor(pygame.sprite.Sprite):
    _screen = None
    _x = 0
    _y = 0
    _w = 0
    _h = 0
    _BoxCollision = None

    def __init__(self, screen, image, x, y, w, h):
        super().__init__()
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._image = image
        self._image = pygame.transform.scale(self._image, (w, h))
        self._screen = screen
        self._BoxCollision = UBoxCollision(self._screen, self._x, self._y, self._w, self._h, "Orange")

    def draw(self):
        self._screen.blit(self._image, (self._x, self._y))
        self._BoxCollision.draw()

    def getActorLocation(self) -> Vector2:
        return Vector2(self._x, self._y)

    def setActorLocation(self, Location: Vector2):
        self._x = Location[0]
        self._y = Location[1]
        self._BoxCollision.setCoordinates(Vector2(self._x, self._y))

    def getCollision(self) -> UBoxCollision:
        return self._BoxCollision
    def Intersects(self, enemy: 'AActor') -> bool:
        if self._BoxCollision is not None and enemy.getCollision() is not None:
            return self._BoxCollision.itteract(enemy.getCollision())
        return False
        


"""
#test AActor game loop

#init game
pygame.init()

#initialize screen object
screen = pygame.display.set_mode((1000,1000))
actor = AActor(screen,"../../assets/cars/pink-car.png",0,0,50,100)
actor1 = AActor(screen,"../../assets/cars/pink-car.png",40,0,50,100)
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
        print(actor.Intersects(actor1))
    screen.fill([255, 255, 255])
    actor.draw()
    actor1.draw()
    #update screen
    pygame.display.update()
    clock.tick(60)
"""