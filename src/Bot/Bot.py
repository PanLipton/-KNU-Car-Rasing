import pygame  # imort pygame module
from sys import exit  # imort sys module
import sys
import os
from pygame.locals import *
from pygame.math import Vector2

sys.path.append("../Actor/")
from Actor.Actor import *


class Bot(AActor):

    def __init__(self, screen, image, x, y, w, h):
        # Load Image
        bot_image_path = os.path.join('..', 'assets', 'cars', image)
        try:
            self.image = pygame.image.load(bot_image_path).convert_alpha()
            self.screen = screen
            # Call AActor Constructor
            super().__init__(self.screen, self.image, x, y, w, h)
            # Drawing
            self.rect = pygame.Rect(x, y, w, h)
        except FileNotFoundError:
            print(f"Error: File not found - {bot_image_path}")
            sys.exit(1)

    def draw(self):
        super().draw()

    # Moving Down
    def MoveDown(self, distance: int):
        cur_Location = super().getActorLocation()
        cur_Location[1] += distance
        super().setActorLocation(cur_Location)


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