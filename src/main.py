import pygame
import sys
from GameController import GameController
def main():
    pygame.init()
    game_controller = GameController()
    game_controller.run()
    pygame.quit()

if __name__ == "__main__":
    main()
