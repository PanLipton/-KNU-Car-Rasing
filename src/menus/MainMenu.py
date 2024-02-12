# MainMenu.py
import pygame
import sys
from menus.BaseMenu import BaseMenu

class MainMenu(BaseMenu):
    def __init__(self, screen, gui_manager, menu_manager, background_image_path):
        super().__init__(screen, gui_manager, menu_manager, background_image_path)
        self.add_button('Play', (self.screen.get_width() // 2 - 100, self.screen.get_height() // 2 - 40), self.play)
        self.add_button('Settings', (self.screen.get_width() // 2 - 100, self.screen.get_height() // 2), self.settings)
        self.add_button('Exit', (self.screen.get_width() // 2 - 100, self.screen.get_height() // 2 + 40), self.exit)

    def play(self):
        print("Play button pressed")

    def settings(self):
        from menus.SettingsMenu import SettingsMenu
        self.menu_manager.change_menu(SettingsMenu)


    def exit(self):
        pygame.quit()
        sys.exit()

    def draw(self):
        super().draw()
        self.gui_manager.draw_ui(self.screen)
