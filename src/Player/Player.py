import pygame #imort pygame module
from sys import exit #imort sys module
import sys
import os
from pygame.locals import *
import math  # Import the math module
from pygame.math import Vector2
import time

sys.path.append('../Actor/')
sys.path.append('../Collision/')
sys.path.append('../SoundManager/')
#sys.path.append('../Bot/')


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



                
    
    def _change_score(self,decimal:int):
        self._score +=decimal
        if(self._score < 0):
            self._score = 0
    def get_score(self)->int:
        return self._score;
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
        #Draw Collision
        #Uncoment if you want 
        #self.BoxCollision.draw()
        
    #Moving Up
    def MoveUP(self,distance:int,obstacles:pygame.sprite.Group()):
        if self._is_explosion_anim_playing:
            return
        cur_Location = super().getActorLocation()
        if ((cur_Location[1]-distance))<0:
            return
        cur_Location[1]-=distance
        if(not (self._Intersects(cur_Location,obstacles) == 1)):
            self._BoxCollision.setCoordinates(cur_Location)
            super().setActorLocation(cur_Location)
    #Moving Down
    def MoveDown(self,distance:int,obstacles:pygame.sprite.Group()):
        if self._is_explosion_anim_playing:
            return
        cur_Location = super().getActorLocation()
        if ((cur_Location[1]-distance))>810:
            return
        cur_Location[1]+=distance
        if(not (self._Intersects(cur_Location,obstacles) == -1)):
            self._BoxCollision.setCoordinates(cur_Location)
            super().setActorLocation(cur_Location)
        
            
    #Moving Right
    def MoveRight(self,distance:int,obstacles:pygame.sprite.Group(), right_edge):
        if self._is_explosion_anim_playing:
            return
        cur_Location = super().getActorLocation()
        if right_edge<=((cur_Location[0]+distance+self._w)):
            return
        cur_Location[0]+=distance
        if(not (self._Intersects(cur_Location,obstacles) == -2)):
            self._BoxCollision.setCoordinates(cur_Location)
            super().setActorLocation(cur_Location)
            
    #Moving Left
    def MoveLeft(self,distance:int,obstacles:pygame.sprite.Group(), left_edge):
        if self._is_explosion_anim_playing:
            return
        cur_Location = super().getActorLocation()
        if ((cur_Location[0]+distance))<=left_edge:
            return
        cur_Location[0]-=distance
        if(not (self._Intersects(cur_Location,obstacles) == 2)):
            self._BoxCollision.setCoordinates(cur_Location)
            super().setActorLocation(cur_Location)
    def _Intersects(self, Location:Vector2,obstacles)->int:
        temp_Collision = UBoxCollision(self._screen,Location[0],Location[1],self._w,self._h,'Orange')
        # Get the current position of the player
        player_location = temp_Collision.getCoordinates()
        # Create a rectangle representing the player's collision box
        player_rect = pygame.Rect(player_location[0], player_location[1], self._w, self._h)

        # Check for intersection with each obstacle
        for obstacle in obstacles:
            # Get the collision box of the obstacle
            obstacle_collision = obstacle.getCollision()

            # Create a rectangle representing the obstacle's collision box
            obstacle_rect = pygame.Rect(obstacle_collision.x, obstacle_collision.y, obstacle_collision.w, obstacle_collision.h)

            # Check for intersection between player's and obstacle's collision boxes
            if player_rect.colliderect(obstacle_rect):
                dx = self._x - obstacle_rect.x
                dy = self._y - obstacle_rect.y
                if abs(dx) > abs(dy):
                    if dx > 0:
                        #right
                        return 2
                    else:
                        #left
                        return -2
                else:
                    if dy > 0:
                        #top
                        return 1
                    else:
                        #bottom
                        return -1
        return 0  # No collision
    
    def update(self,obstacles)->bool:
        # Якщо анімація вибуху вже грає, продовжуємо її відтворення
        if self._is_explosion_anim_playing:
            self._play_explosion_animation(self._x, self._y)
            return False  # Повертаємо False, щоб індикувати, що гравець зараз не може взаємодіяти

        # Перевірка на зіткнення
        direction = self._Intersects(super().getActorLocation(), obstacles)
        if direction != 0:
            # Зіткнення відбулося, і анімація вибуху ще не грає
            self._SoundManager.playSoundCrash()
            self._play_explosion_animation(self._x, self._y)
            
            # Після запуску анімації вибуху, перевіряємо, чи вона все ще грає
            if not self._is_explosion_anim_playing:
                # Якщо анімація завершилась, встановлюємо гравця як неактивного
                self.is_active = False
                return True  # Повертаємо True, щоб індикувати, що сталося зіткнення і стан гравця змінився
        elif(direction ==2):
            self._change_score(-3)
            return False
        elif(direction ==-2):
            self._change_score(-3)
            return False
        return False
            
        

"""
#test APlayer game loop

#init game
pygame.init()

#initialize screen object
screen = pygame.display.set_mode((1000,1000))

all_sprites = pygame.sprite.Group()

player = APlayer(screen,"pink-car.png",300,500,50,100)
bot = Bot(screen,"pink-car.png",250,100,50,100)
bot1 = Bot(screen,"pink-car.png",400,100,50,100)

all_sprites.add(bot,bot1)
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
            player.MoveLeft(10, all_sprites)
        if keys[K_RIGHT]:
            player.MoveRight(10, all_sprites)
        if keys[K_DOWN]:
            player.MoveDown(10, all_sprites)
        if keys[K_UP]:
            player.MoveUP(10, all_sprites)
    player.update(all_sprites)
    for bot in all_sprites:
        bot.MoveDown(1)
    screen.fill([255, 255, 255])
    player.draw()
    for bot in all_sprites:
        bot.draw()
    #update screen
    pygame.display.update()
    clock.tick(60)

"""
