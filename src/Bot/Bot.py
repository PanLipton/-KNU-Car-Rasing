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

class Bot(AActor):
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
        self.BoxCollision = UBoxCollision(self.screen,x,y,w,h,'Orange')
        #Drawing 
    def draw(self):
        super().draw()
        #Draw Collision
        #Uncoment if you want 
        self.BoxCollision.draw()
    #Moving Down
    def MoveDown(self,distance:int):
        cur_Location = super().getActorLocation()
        cur_Location[1]+=distance
        self.BoxCollision.setCoordinates(cur_Location)
        super().setActorLocation(cur_Location)
    def getCollision(self)->UBoxCollision:
        return self.BoxCollision

"""
#test APlayer game loop

#init game
pygame.init()

#initialize screen object
screen = pygame.display.set_mode((1000,1000))

bot = Bot(screen,"pink-car.png",150,50,50,100)

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
        if keys[K_DOWN]:
            bot.MoveDown(10)
    
    screen.fill([255, 255, 255])
    bot.draw()
    #update screen
    pygame.display.update()
    clock.tick(60)
"""
