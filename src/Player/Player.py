import pygame #imort pygame module
from sys import exit #imort sys module
import sys
import os
from pygame.locals import *
import math  # Import the math module
from pygame.math import Vector2
#pyganim module
#import pyganim

sys.path.append('../Actor/')
sys.path.append('../Collision/')
sys.path.append('../SoundManager/')


from Collision.Collision import *
from Actor.Actor import *
from SoundManager.SoundManager import *

class APlayer(AActor):
    #private
    _BoxCollision=None
    _SoundManager=None
    _score = None
    _explosion_animation = None

    
    def __init__(self,screen,image,x,y,w,h):
        #Load Image
        try:
            self._image = pygame.image.load(image).convert_alpha()
        except FileNotFoundError:
            print(f"Error: File not found - {image}")
            sys.exit(1)

        self._image = pygame.transform.scale(self._image, (w, h))
        self._screen = screen
        #Call AActor Constructor
        super().__init__(self._screen,self._image,x,y,w,h)
        #Create Box Collision
        self._BoxCollision = UBoxCollision(self._screen,x,y,w,h,'Orange')
        self._SoundManager = SoundManager()
        # Load explosion frames/images
        self._score = 0
        self._load_explosion_frames("explosion.png", 512, 512)


    #Load explosion animations
    def _load_explosion_frames(self, exp_image, frame_width, frame_height):
        self._explosion_animation = []  # Initialize the list to store explosion frames
        # Прямий шлях до зображення вибуху
        exp_image_path = os.path.join('..','assets', 'animations', 'explosion', exp_image)
        try:
            explosion_sheet = pygame.image.load(exp_image_path).convert_alpha()
            sheet_width, sheet_height = explosion_sheet.get_size()
            rows = sheet_height // frame_height
            cols = sheet_width // frame_width
            for y in range(rows):
                for x in range(cols):
                    frame = explosion_sheet.subsurface(pygame.Rect(x * frame_width, y * frame_height, frame_width, frame_height))
                    self._explosion_animation.append(frame)
        except FileNotFoundError:
            print(f"Error: File not found - {exp_image_path}")
            sys.exit(1)


    #Play explosion animations
    def _play_explosion_animation(self, player_x, player_y):
        if self._explosion_animation:
            for frame in self._explosion_animation:
                frame_rect = frame.get_rect()
                frame_rect.center = (player_x, player_y)
                frame_x = frame_rect.topleft[0]+ self._w/2
                frame_y = frame_rect.topleft[1]+ self._h/2
                # Set the frame's center to match player's position
                self._screen.blit(frame, (frame_x,frame_y))  # Blit the frame at the adjusted position
                pygame.display.flip()  # Update the display after blitting each frame
                pygame.time.wait(50)  # Adjust the delay between frames as needed


    def _change_score(self,decimal:int):
        self._score +=decimal
        if(self._score < 0):
            self._score = 0
    def get_score(self)->int:
        return self._score;
    #Drawing 
    def draw(self):
        super().draw()
        #TODO: Play Sound of engine
        #self._SoundManager.playSoundCar()
        #Draw Collision
        #Uncoment if you want 
        #self.BoxCollision.draw()
        
    #Moving Up
    def MoveUP(self,distance:int,obstacles:pygame.sprite.Group())->bool:
        cur_Location = super().getActorLocation()
        if ((cur_Location[1]-distance))<0:
            return
        cur_Location[1]-=distance
        if(not self.Intersects(cur_Location,obstacles)):
            self._BoxCollision.setCoordinates(cur_Location)
            super().setActorLocation(cur_Location)
            self._SoundManager.playSoundVroom()
            return False
        self._SoundManager.playSoundCrash()
        self._play_explosion_animation(self._x,self._y)

        return True
    #Moving Down
    def MoveDown(self,distance:int,obstacles:pygame.sprite.Group())->bool:
        cur_Location = super().getActorLocation()
        if ((cur_Location[1]-distance))>810:
            return
        cur_Location[1]+=distance
        if(not self.Intersects(cur_Location,obstacles)):
            self._BoxCollision.setCoordinates(cur_Location)
            super().setActorLocation(cur_Location)
            self._SoundManager.playSoundStop()
            return False
        self._SoundManager.playSoundCrash()
        self._play_explosion_animation(self._x,self._y)

        return True
            
    #Moving Right
    def MoveRight(self,distance:int,obstacles:pygame.sprite.Group(), right_edge):
        cur_Location = super().getActorLocation()
        if right_edge<=((cur_Location[0]+distance+self._w)):
            return
        cur_Location[0]+=distance
        if(not self.Intersects(cur_Location,obstacles)):
            self._BoxCollision.setCoordinates(cur_Location)
            super().setActorLocation(cur_Location)
            self._SoundManager.playSoundLineChange()
        # print(self._score)
            
    #Moving Left
    def MoveLeft(self,distance:int,obstacles:pygame.sprite.Group(), left_edge):
        cur_Location = super().getActorLocation()
        if ((cur_Location[0]+distance))<=left_edge:
            return
        cur_Location[0]-=distance
        if(not self.Intersects(cur_Location,obstacles)):
            self._BoxCollision.setCoordinates(cur_Location)
            super().setActorLocation(cur_Location)
            self._SoundManager.playSoundLineChange()
        # print(self._score)
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

