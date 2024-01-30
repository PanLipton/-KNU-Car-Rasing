import pygame #imort pygame module
from sys import exit #imort sys module
import sys
import os
from pygame.locals import *
import math  # Import the math module
from pygame.math import Vector2

sys.path.append("../Collision/")

from Collision import *

class AActor(pygame.sprite.Sprite):
    screen=None
    BoxCollision=None

    def __init__(self,screen,image,x,y,w,h):
        super().__init__()
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.BoxCollision = UBoxCollision(screen,x,y,w,h,"Orange")
        self.rect = pygame.Rect(x,y,w,h)
        script_directory = os.path.dirname(os.path.abspath("../"))
        player_image_path = os.path.join("assets/cars",image)
        self.image = pygame.image.load(os.path.join(script_directory, player_image_path))
        self.FRotator = Vector2(1, 0)
    # TODO: fix rotation
    def draw(self):
        # Calculate the rotation angle based on the FRotator
        angle = math.degrees(math.atan2(-self.FRotator.y, self.FRotator.x))
        rotated_image = pygame.transform.rotate(self.image, angle)
        rotated_rect = rotated_image.get_rect(center=self.rect.center)

        # Adjust midtop position based on rotation
        rotated_midtop = rotated_rect.midtop
        offset = Vector2(self.rect.midtop) - Vector2(rotated_midtop)
        rotated_rect.midtop += offset

        # Blit the rotated image using the new midtop position
        screen.blit(rotated_image, rotated_rect.center)


    def getActorLocation(self)->Vector2:
        return Vector2(self.rect.center)
    def setActorLocation(self,Location:Vector2):
        self.rect.center = Location
    def getActorRotation(self)->Vector2:
        return self.FRotator
    def setActorRotation(self, FRotator: Vector2):
        self.FRotator = FRotator
    def FindLookAtRotation(self,Start:Vector2,End:Vector2)->Vector2:
        direction_vector = End - Start
        return direction_vector.normalize()


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
    target_point = Vector2(500,500)

    # Find rotation vector towards the target point
    player_rotation_vector = actor.FindLookAtRotation(actor.getActorLocation(), target_point)

    # Set player rotation based on the rotation vector
    actor.setActorRotation(player_rotation_vector)
    
    screen.fill([255, 255, 255])
    actor.draw()
    #update screen
    pygame.display.update()
    clock.tick(60)
"""
