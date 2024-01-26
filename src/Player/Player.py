import pygame #imort pygame module
from sys import exit #imort sys module
import sys
import os
from pygame.locals import *
import math  # Import the math module
from pygame.math import Vector2

sys.path.append("../Actor/")
sys.path.append("../Collision/")

from Collision import *
from Actor import *

class APlayer(AActor):
    BoxCollision=None
    def __init__(self,screen,image,x,y,w,h):
        #Load Image
        script_directory = os.path.dirname(os.path.abspath("../"))
        player_image_path = os.path.join("assets/cars",image)
        self.image = pygame.image.load(os.path.join(script_directory, player_image_path))
        self.screen = screen
        #Call AActor Constructor
        super().__init__(self.screen,self.image,x,y,w,h)
        #Create Box Collision
        self.BoxCollision = UBoxCollision(screen,x,y,w,h,'Orange')
    #Drawing 
    def draw(self):
        super().draw()
        #Draw Collision
        #Uncoment if you want 
        #self.BoxCollision.draw()
    #Moving Up
    def MoveUP(self,distance:int):
        cur_Location = super().getActorLocation()
        cur_Location[1]-=distance
        self.BoxCollision.setCoordinates(cur_Location)
        super().setActorLocation(cur_Location)
    #Moving Down
    def MoveDown(self,distance:int):
        cur_Location = super().getActorLocation()
        cur_Location[1]+=distance
        self.BoxCollision.setCoordinates(cur_Location)
        super().setActorLocation(cur_Location)
    #Moving Right
    def MoveRight(self,distance:int):
        cur_Location = super().getActorLocation()
        cur_Location[0]+=distance
        self.BoxCollision.setCoordinates(cur_Location)
        super().setActorLocation(cur_Location)
    #Moving Left
    def MoveLeft(self,distance:int):
        cur_Location = super().getActorLocation()
        cur_Location[0]-=distance
        self.BoxCollision.setCoordinates(cur_Location)
        super().setActorLocation(cur_Location)
    def Intersects(collision:UBoxCollision):
        if(self.BoxCollision.simple_itteract(collision)):
            
        


"""
#test APlayer game loop

#init game
pygame.init()

#initialize screen object
screen = pygame.display.set_mode((1000,1000))
player = APlayer(screen,"pink-car.png",150,50,50,100)
left = UBoxCollision(screen,0,0,100,1000,"Orange")
right = UBoxCollision(screen,900,0,100,1000,"Orange")
clock = pygame.time.Clock()
#Title
pygame.display.set_caption("Car Racing")


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
        if keys[K_LEFT]:
            player.MoveLeft(5)
        if keys[K_RIGHT]:
            player.MoveRight(5)
        if keys[K_DOWN]:
            player.MoveDown(5)
        if keys[K_UP]:
            player.MoveUP(5)
    
    screen.fill([255, 255, 255])
    player.draw()
    left.draw()
    right.draw()
    #update screen
    pygame.display.update()
    clock.tick(60)
"""