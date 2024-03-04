import pygame #imort pygame module
from sys import exit #imort sys module
import sys
import os
from pygame.locals import *
import math  # Import the math module
from pygame.math import Vector2
import time

sys.path.append('../Actor/')
sys.path.append('../SoundManager/')

from Actor.Actor import *
from SoundManager.SoundManager import *

class APlayer(AActor):
    #private
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
        self._SoundManager = SoundManager()
        # Load explosion frames/images
        self._score = 0
        self._load_explosion_frames("explosion.png", 512, 512)
        self.is_active = True  # Гравець активний на початку гри
        self._last_frame_time = None
        self._animation_frame_index = 0
        self._is_explosion_anim_playing = False
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
        if not self._is_explosion_anim_playing:
            self._is_explosion_anim_playing = True
            self._animation_frame_index = 0
            self._last_frame_time = time.time()

        if self._is_explosion_anim_playing:
            if time.time() - self._last_frame_time >= 0.05:
                frame = self._explosion_animation[self._animation_frame_index]
                frame_rect = frame.get_rect()
                
                # Розрахунок позиції кадру так, щоб центр кадру співпадав з центром машини гравця
                frame_x = player_x + (self._w / 2) - (frame_rect.width / 2)
                frame_y = player_y + (self._h / 2) - (frame_rect.height / 2)

                self._screen.blit(frame, (frame_x, frame_y))
                pygame.display.flip()

                self._last_frame_time = time.time()
                self._animation_frame_index += 1

                if self._animation_frame_index >= len(self._explosion_animation):
                    self._is_explosion_anim_playing = False
                    self._animation_frame_index = 0
                    self.is_active = False

    def change_score(self,decimal:int):
        self._score +=decimal
        if(self._score < 0):
            self._score = 0
    def get_score(self)->int:
        return self._score
    def draw_explosion(self):
        if self._is_explosion_anim_playing and self._animation_frame_index < len(self._explosion_animation):
            frame = self._explosion_animation[self._animation_frame_index]
            frame_rect = frame.get_rect()
            frame_rect.center = (self._x + self._w / 2, self._y + self._h / 2)

            self._screen.blit(frame, frame_rect.topleft)
            self._last_frame_time = pygame.time.get_ticks()
    #Drawing 
    def draw(self):
        super().draw()
    #Moving Up
    def MoveUP(self,distance:int,obstacles=[]):
        cur_Location = super().getActorLocation()
        cur_Location[1]-=distance
        temp_Collision = UBoxCollision(self._screen,cur_Location[0],cur_Location[1],self._w,self._h,'Orange')
        collision_detected = False
        if(not (len(obstacles) == 0)):
            for obstacle in obstacles:
                if(temp_Collision.itteract(obstacle)):
                    collision_detected = True
                    break

        if(not collision_detected):
            super().setActorLocation(cur_Location)
    #Moving Down
    def MoveDown(self,distance:int,obstacles=[]):
        cur_Location = super().getActorLocation()
        cur_Location[1]+=distance
        temp_Collision = UBoxCollision(self._screen,cur_Location[0],cur_Location[1],self._w,self._h,'Orange')
        collision_detected = False
        if(not (len(obstacles) == 0)):
            for obstacle in obstacles:
                if(temp_Collision.itteract(obstacle)):
                    collision_detected = True
                    break

        if(not collision_detected):
            super().setActorLocation(cur_Location)
            
    #Moving Right
    def MoveRight(self,distance:int,obstacles=[]):
        cur_Location = super().getActorLocation()
        cur_Location[0]+=distance
        temp_Collision = UBoxCollision(self._screen,cur_Location[0],cur_Location[1],self._w,self._h,'Orange')
        collision_detected = False
        if(not (len(obstacles) == 0)):
            for obstacle in obstacles:
                if(temp_Collision.itteract(obstacle)):
                    collision_detected = True
                    break

        if(not collision_detected):
            super().setActorLocation(cur_Location)
            
    #Moving Left
    def MoveLeft(self,distance:int,obstacles=[]):
        cur_Location = super().getActorLocation()
        cur_Location[0]-=distance
        temp_Collision = UBoxCollision(self._screen,cur_Location[0],cur_Location[1],self._w,self._h,'Orange')
        collision_detected = False
        if(not (len(obstacles) == 0)):
            for obstacle in obstacles:
                if(temp_Collision.itteract(obstacle)):
                    collision_detected = True
                    break

        if(not collision_detected):
            super().setActorLocation(cur_Location)
    def update(self,enemies:pygame.sprite.Group()):
        for enemy in enemies:
            if(self!=enemy):
                if(super().Intersects(enemy)):
                    self._SoundManager.playSoundCrash()
                    self._play_explosion_animation(self._x,self._y)
                    return True
        return False
    
        

"""
#test APlayer game loop

#init game
pygame.init()

#initialize screen object
screen = pygame.display.set_mode((1000,1000))
#Sprite Groups for enemies
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
#Obstacles
obstacles = []
left = UBoxCollision(screen,0,0,100,1000,'Orange')
right = UBoxCollision(screen,900,0,100,1000,'Orange')
top = UBoxCollision(screen,100,0,900,100,'Orange')
bottom = UBoxCollision(screen,100,800,800,100,'Orange')
obstacles.append(right)
obstacles.append(left)
obstacles.append(top)
obstacles.append(bottom)

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
            player.MoveLeft(10,obstacles)
        if keys[K_RIGHT]:
            player.MoveRight(10,obstacles)
        if keys[K_DOWN]:
            player.MoveDown(10,obstacles)
        if keys[K_UP]:
            player.MoveUP(10,obstacles)
    player.update(all_sprite)
    for bot in bot_actors:
        bot.MoveDown(1)
    screen.fill([255, 255, 255])
    player.draw()
    player1.draw()
    for bot in bot_actors:
        bot.draw()
    for collision in obstacles:
        collision.draw()
    #update screen
    pygame.display.update()
    clock.tick(60)
    
"""
