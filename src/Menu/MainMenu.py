# MainMenu.py
import pygame
import sys
from Menu.BaseMenu import BaseMenu

class MainMenu(BaseMenu):
    def __init__(self, screen, gui_manager, menu_manager, background_image_path):
        title_font = pygame.font.Font('../assets/fonts/pixel_font.ttf', 100)  # Задаємо шрифт для заголовку
        super().__init__(screen, gui_manager, menu_manager, background_image_path, "Car Racing", title_font) 
        self.add_button('Play', (self.screen.get_width() // 2 - 100, self.screen.get_height() // 2 - 40), self.play, 'no_border_button')
        self.add_button('Settings', (self.screen.get_width() // 2 - 100, self.screen.get_height() // 2), self.settings, 'no_border_button')
        self.add_button('Exit', (self.screen.get_width() // 2 - 100, self.screen.get_height() // 2 + 40), self.exit, 'no_border_button')

    def play(self):
<<<<<<< HEAD
        from Menu.PlayerSelectionMenu import PlayerSelectionMenu
        self.menu_manager.change_menu(PlayerSelectionMenu)
=======
        print("Play button pressed")
>>>>>>> main

    def settings(self):
        from Menu.SettingsMenu import SettingsMenu
        self.menu_manager.change_menu(SettingsMenu)


    def exit(self):
        pygame.quit()
        sys.exit()

    def draw(self):
        super().draw()
        self.gui_manager.draw_ui(self.screen)
