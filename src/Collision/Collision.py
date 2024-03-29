import pygame  # imort pygame module
from sys import exit  # imort sys module
from pygame.locals import *
from pygame.math import Vector2
from config import DEBUG


# BoxCollision class: This class defines a basic collision which is uded in Character
# To write a login on collision events

class UBoxCollision(pygame.Rect):
    # width of BoxCollision
    w = 0
    h = 0
    # position of BoxCollision
    x = 0
    y = 0
    # Window
    screen = None
    # Color
    color = None

    # Constructor
    def __init__(self, screen, x, y, w, h, color):
        super().__init__(x, y, w, h)
        # Size
        self.w = w
        self.h = h
        # Position
        self.x = x
        self.y = y
        # Color
        self.color = color
        # Screen
        self.screen = screen
        # Set Width
        self.surf = pygame.Surface((w, h))
        # Define the color of the surface
        self.surf.fill(color)

    # draw Collision (May be used in Debug mode)
    def draw(self):
        if DEBUG:
            pygame.draw.rect(self.screen, self.color, self, 2)
            
    # Check Collision itteraction
    def itteract(self, collision: 'UBoxCollision'):
        return self.colliderect(collision)

    def setCoordinates(self, NewCoordinates: Vector2):
        self.x = NewCoordinates[0]
        self.y = NewCoordinates[1]
        self._updateRect()

    def _updateRect(self):
        # Update rectangle coordinates
        self.left = self.x
        self.top = self.y


"""
#test Collision game loop

#init game
pygame.init()

#initialize screen object
screen = pygame.display.set_mode((1000,1000))
collision = UBoxCollision(screen,50,0,50,100,'White')
collision1 = UBoxCollision(screen,50,130,50,100,'White')
clock = pygame.time.Clock()
collision.setCoordinates((200,300))
print(collision1.itteract(collision))

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
    collision.draw()
    collision1.draw()
    #update screen
    pygame.display.update()
    clock.tick(60)

"""