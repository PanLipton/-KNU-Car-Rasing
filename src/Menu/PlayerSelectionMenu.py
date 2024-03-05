# PlayerSelectionMenu.py

import pygame
from Menu.BaseMenu import BaseMenu
from pathlib import Path

class PlayerSelectionMenu(BaseMenu):
    def __init__(self, screen, gui_manager, menu_manager, background_image_path):
        title_font = pygame.font.Font(Path('../assets/fonts/pixel_font.ttf'), 100)
        super().__init__(screen, gui_manager, menu_manager, background_image_path, "Number of players", title_font)
        self.create_ui()

    def create_ui(self):
        positions = [(self.screen.get_width() // 2 - 100, self.screen.get_height() // 2 - 90 + i * 40) for i in range(3)]
        for i, pos in enumerate(positions, start=1):
            self.add_button(f'{i} Player' if i == 1 else f'{i} Players', pos, lambda i=i: self.select_players(i), 'no_border_button')
        self.add_button('Back', (self.screen.get_width() // 2 - 100, self.screen.get_height() // 2 + 30), self.back_action, 'no_border_button')

    def select_players(self, num_players):
        self.menu_manager.set_num_players(num_players)
        self.start_game(num_players)  # Запуск гри з вибраною кількістю гравців

    def back_action(self):
        from Menu.MainMenu import MainMenu
        self.menu_manager.change_menu(MainMenu)

    def start_game(self, num_players):
        from GameScene import GameScene
        self.game_scene = GameScene(self.screen, num_players)
        self.game_scene.run()
    
    def draw(self):
        super().draw()
        self.gui_manager.draw_ui(self.screen)
