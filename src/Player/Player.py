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
sys.path.append('../SoundManager/')
sys.path.append('../Bot/')

from Bot import *
from Actor import *
from SoundManager import *

class APlayer(AActor):
    #private
    _SoundManager=None
    _score = None
    _explosion_animation = None

    
    def __init__(self,screen,image,x,y,w,h):
        #Load Image
        script_directory = os.path.dirname(os.path.abspath("../"))
        player_image_path = os.path.join("assets/cars",image)
        self._image = pygame.image.load(os.path.join(script_directory, player_image_path))
        self._screen = screen
        #Call AActor Constructor
        super().__init__(self._screen,self._image,x,y,w,h)
        self._SoundManager = SoundManager()
        # Load explosion frames/images
        self._score = 0
        self._load_explosion_frames("explosion.png",512,512)


    #Load explosion animations
    def _load_explosion_frames(self, exp_image, frame_width, frame_height):
        self._explosion_animation = []  # Initialize the list to store explosion frames
        script_directory = os.path.dirname(os.path.abspath("../"))  # Get the directory of the current script
        player_image_path = os.path.join("assets/animations/explosion",exp_image)
        exp_image_path = os.path.join(script_directory, player_image_path)  # Construct the path to the explosion image
        print("Explosion image path:", exp_image_path)
        explosion_sheet = pygame.image.load(exp_image_path).convert_alpha()  # L
        sheet_width, sheet_height = explosion_sheet.get_size()
        rows = sheet_height // frame_height
        cols = sheet_width // frame_width
        for y in range(rows):
            for x in range(cols):
                frame = explosion_sheet.subsurface(pygame.Rect(x * frame_width, y * frame_height, frame_width, frame_height))
                self._explosion_animation.append(frame)



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


    def get_score(self)->int:
        return self._score;
    #Drawing 
    def draw(self):
        super().draw()
    #Moving Up
    def MoveUP(self,distance:int):
        cur_Location = super().getActorLocation()
        cur_Location[1]-=distance
        super().setActorLocation(cur_Location)
    #Moving Down
    def MoveDown(self,distance:int):
        cur_Location = super().getActorLocation()
        cur_Location[1]+=distance
        super().setActorLocation(cur_Location)
            
    #Moving Right
    def MoveRight(self,distance:int):
        cur_Location = super().getActorLocation()
        cur_Location[0]+=distance
        super().setActorLocation(cur_Location)
            
    #Moving Left
    def MoveLeft(self,distance:int):
        cur_Location = super().getActorLocation()
        cur_Location[0]-=distance
        super().setActorLocation(cur_Location)
    def update(self,obstacles:pygame.sprite.Group()):
        for enemy in obstacles:
            if(self!=enemy):
                if(super().Intersects(enemy)):
                    self._SoundManager.playSoundCrash()
                    self._play_explosion_animation(self._x,self._y)
                    return True
        return False
    
        



#test APlayer game loop

#init game
pygame.init()

#initialize screen object
screen = pygame.display.set_mode((1000,1000))
all_sprite = pygame.sprite.Group()
player_actors = pygame.sprite.Group()
bot_actors = pygame.sprite.Group()
player = APlayer(screen,"pink-car.png",300,500,50,100)
player1 = APlayer(screen,"pink-car.png",300,100,50,100)
bot = Bot(screen,"pink-car.png",250,100,50,100)
bot1 = Bot(screen,"pink-car.png",450,100,50,100)

player_actors.add(player,player1)
bot_actors.add(bot,bot1)
all_sprite.add(player_actors,bot_actors)
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
            player.MoveLeft(10)
        if keys[K_RIGHT]:
            player.MoveRight(10)
        if keys[K_DOWN]:
            player.MoveDown(10)
        if keys[K_UP]:
            player.MoveUP(10)
    player.update(all_sprite)
    for bot in bot_actors:
        bot.MoveDown(1)
    screen.fill([255, 255, 255])
    player.draw()
    player1.draw()
    for bot in bot_actors:
        bot.draw()
    #update screen
    pygame.display.update()
    clock.tick(60)


