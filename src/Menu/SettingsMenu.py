# SettingsMenu.py

import pygame
import pygame_gui
from Menu.BaseMenu import BaseMenu
from pathlib import Path

class SettingsMenu(BaseMenu):
    def __init__(self, screen, gui_manager, menu_manager, background_image_path):
        title_font = pygame.font.Font(Path('../assets/fonts/pixel_font.ttf'), 100)  # Задаємо шрифт для заголовку
        super().__init__(screen, gui_manager, menu_manager, background_image_path, "Car Racing", title_font)
        self.create_ui_elements()

    def create_ui_elements(self):
        # Створення мітки "Volume"
        self.volume_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.screen.get_width() // 2 - 100, self.screen.get_height() // 2 - 80), (200, 30)),
            text='Volume',
            manager=self.gui_manager,
            container=self.gui_manager.get_root_container(),
            object_id='no_border_label'
        )

        # Створення слайдера гучності
        self.volume_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((self.screen.get_width() // 2 - 100, self.screen.get_height() // 2 - 40), (200, 20)),
            start_value=50,
            value_range=(0, 100),
            manager=self.gui_manager,
            container=self.gui_manager.get_root_container(),
            object_id='no_border_slider'
        )

        # Створення кнопки "Back" за допомогою методу add_button
        self.add_button('Back', (self.screen.get_width() // 2 - 100, self.screen.get_height() // 2), self.back_action, 'no_border_button')

    def back_action(self):
        from Menu.MainMenu import MainMenu
        self.menu_manager.change_menu(MainMenu)

    def draw(self):
        super().draw()
        self.gui_manager.draw_ui(self.screen)

    def handle_event(self, event):
        super().handle_event(event)
        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == self.volume_slider:
                print(f"Volume set to {event.value}")
