import pygame #imort pygame module
from sys import exit #imort sys module
import sys
import os
from pygame.locals import *
import math  # Import the math module
from pygame.math import Vector2

sys.path.append("../Actor/")
sys.path.append("../Collision/")
sys.path.append("../SoundManager/")

from Collision import *
from Actor import *
from SoundManager import *

class APlayer(AActor):
    #private
    _BoxCollision=None
    _SoundManager=None
    def __init__(self,screen,image,x,y,w,h):
        #Load Image
        script_directory = os.path.dirname(os.path.abspath("../"))
        player_image_path = os.path.join("assets/cars",image)
        self._image = pygame.image.load(os.path.join(script_directory, player_image_path))
        self._screen = screen
        #Call AActor Constructor
        super().__init__(self._screen,self._image,x,y,w,h)
        #Create Box Collision
        self._BoxCollision = UBoxCollision(self._screen,x,y,w,h,'Orange')
        self._SoundManager = SoundManager()

    #Drawing 
    def draw(self):
        super().draw()
        #TODO: Play Sound of engine
        #self.SoundManager.playSoundCar()
        #Draw Collision
        #Uncoment if you want 
        #self.BoxCollision.draw()
        
    #Moving Up
    def MoveUP(self,distance:int,obstacles:pygame.sprite.Group())->bool:
        cur_Location = super().getActorLocation()
        cur_Location[1]-=distance
        if(not self.Intersects(cur_Location,obstacles)):
            self._BoxCollision.setCoordinates(cur_Location)
            super().setActorLocation(cur_Location)
            return False
        self._SoundManager.playSoundCrash()
        return True
    #Moving Down
    def MoveDown(self,distance:int,obstacles:pygame.sprite.Group())->bool:
        cur_Location = super().getActorLocation()
        cur_Location[1]+=distance
        if(not self.Intersects(cur_Location,obstacles)):
            self._BoxCollision.setCoordinates(cur_Location)
            super().setActorLocation(cur_Location)
            return False
        self._SoundManager.playSoundCrash()
        return True
            
    #Moving Right
    def MoveRight(self,distance:int,obstacles:pygame.sprite.Group()):
        cur_Location = super().getActorLocation()
        cur_Location[0]+=distance
        if(not self.Intersects(cur_Location,obstacles)):
            self._BoxCollision.setCoordinates(cur_Location)
            super().setActorLocation(cur_Location)
            
    #Moving Left
    def MoveLeft(self,distance:int,obstacles:pygame.sprite.Group()):
        cur_Location = super().getActorLocation()
        cur_Location[0]-=distance
        if(not self.Intersects(cur_Location,obstacles)):
            self._BoxCollision.setCoordinates(cur_Location)
            super().setActorLocation(cur_Location)
    #BoxCollision getter
    def getCollision(self):
        return self._BoxCollision
    #Intersects with BoxCollision
    def Intersects(self,Location:Vector2,obstacles:pygame.sprite.Group()):
        temp_Collision = UBoxCollision(self._screen,Location[0],Location[1],self._w,self._h,'Orange')
        for sprite in obstacles:
            if(not sprite == self):
                if(temp_Collision.itteract(sprite.getCollision())):
                    return True
        return False
    #handle Player keys reaction returns true if Player intersects from front and back 
    def handle_events(self,distance:int,obstacles:pygame.sprite.Group())->bool:
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            player.MoveLeft(distance,obstacles)
        if keys[K_RIGHT]:
            player.MoveRight(distance,obstacles)
        if keys[K_DOWN]:
            return player.MoveDown(distance,obstacles)
        if keys[K_UP]:
            return player.MoveUP(distance,obstacles)
        

            
        
"""
#test APlayer game loop

#init game
pygame.init()

#initialize screen object
screen = pygame.display.set_mode((1000,1000))

all_sprites = pygame.sprite.Group()

player = APlayer(screen,"pink-car.png",150,50,50,100)
player1 = APlayer(screen,"pink-car.png",250,100,50,100)
player2 = APlayer(screen,"pink-car.png",350,150,50,100)

all_sprites.add(player,player1,player2)
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
        print(player.handle_events(10,all_sprites))
    
    screen.fill([255, 255, 255])
    player.draw()
    player1.draw()
    player2.draw()
    #update screen
    pygame.display.update()
    clock.tick(60)
"""
