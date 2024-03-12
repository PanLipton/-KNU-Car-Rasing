# main.py
import argparse
import pygame
import config

from GameController import GameController

def main(debug=False):
    game_controller = GameController(debug=debug)
    game_controller.run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', help="Enable debug mode to display collisions")
    args = parser.parse_args()

    config.DEBUG = args.debug

    main(debug=args.debug)
    pygame.quit()
