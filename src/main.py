# main.py
import pygame
from GameController import GameController

def main():
    game_controller = GameController()
    game_controller.run()

if __name__ == "__main__":
    main()
    pygame.quit()