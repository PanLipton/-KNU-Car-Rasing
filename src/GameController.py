import pygame
import pygame_gui
import sys
from Menu.Interface import *
sys.path.append("Road/")
# sys.path.append("Player/")

from Road import *
# from Menu import *
# from Player import *

class GameController:
    # def __init__(self):
    #     pygame.init()
    #     self.screen_width = 1366
    #     self.screen_height = 900
    #     pygame.display.set_caption('Car Racing')

    #     # Опции меню
    #     self.menu_items = ['Play', 'Settings', 'Exit']
        
    #     self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
    #     self.running = True
    #     self.state = "menu"

    #     # Загрузка пиксельного шрифта
    #     self.title_font = pygame.font.Font('../assets/fonts/pixel_font.ttf', 100)
    #     self.pixel_font = pygame.font.Font('../assets/fonts/pixel_font.ttf', 20)  

    #     # Загрузка фонового изображения    
    #     self.background = pygame.image.load('../assets/img/backgroundimg.jpg')

    #     self.gui_manager = pygame_gui.UIManager((self.screen.get_width(), self.screen.get_height()), 'theme.json')

    #     self.menu = BaseMenu(self.screen, self.title_font, self.pixel_font, self.background)
    #     self.menu = MainMenu(self.screen, self.title_font, self.pixel_font, self.background) 
    #      # Ініціалізація головного меню
    #     self.settings = SettingsMenu(self.screen, self.title_font, self.pixel_font, self.background)  # Ініціалізація меню налаштувань
    #     self.game = None  # Ігровий стан буде ініціалізовано пізніше

    # def initialize_game(self):
    #     # Словник з зображеннями доріг для різної кількості гравців
    #     roads_images = {
    #     1: '../assets/img/road-5-lines.png',
    #     2: '../assets/img/road-6-lines.png',
    #     }
    #     player_count = 1
    #     selected_road_image = roads_images.get(player_count, '../assets/img/road-5-lines.png')  
    #     # Ініціалізація компонентів гри
    #     self.road1 = Road(selected_road_image, self.screen_width, self.screen_height)
    #     self.road2 = Road(selected_road_image, self.screen_width, self.screen_height)
    #     self.road2.rect.y = -self.road2.rect.height
    #     # Ініціалізація машин гравців
    #     self.players = [APlayer(self.screen, 'car_image.png', 100, 100, 50, 100) for _ in range(self.player_count)]
    #     # Інші компоненти гри

    def initialize_settings(self):
        # Ініціалізація інтерфейсу налаштувань
        self.settings = SettingsMenu(self.screen, self.title_font, self.pixel_font, self.background)

    def run(self):
        while self.running:
            if self.state == "menu":
                self.menu_loop()
            elif self.state == "game":
                self.game_loop()
            elif self.state == "settings":
                self.settings_loop()
            else:
                self.running = False


# Головна точка входу
if __name__ == "__main__":
    game_controller = GameController()
    game_controller.run()
    pygame.quit()
    sys.exit()
