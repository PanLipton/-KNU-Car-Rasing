# SettingsMenu.py

import pygame
import pygame_gui
from Menu.BaseMenu import BaseMenu

from src.SoundManager.SoundManager import sound_manager


class SettingsMenu(BaseMenu):
    def __init__(self, screen, gui_manager, menu_manager, background_image_path):
        title_font = pygame.font.Font('../assets/fonts/pixel_font.ttf', 100)
        super().__init__(screen, gui_manager, menu_manager, background_image_path, "Car Racing", title_font)
        self.volume = 50  # Початкове значення гучності
        self.create_ui_elements()

    def create_ui_elements(self):
        self.volume_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.screen.get_width() // 2 - 100, self.screen.get_height() // 2 - 80), (200, 30)),
            text='Volume',
            manager=self.gui_manager,
            container=self.gui_manager.get_root_container(),
            object_id='no_border_label'
        )

        self.volume_display = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.screen.get_width() // 2 + 120, self.screen.get_height() // 2 - 80), (50, 30)),
            text=str(self.volume),  # Відображення поточного значення гучності
            manager=self.gui_manager,
            container=self.gui_manager.get_root_container(),
            object_id='no_border_label'
        )

        self.lower_volume_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screen.get_width() // 2 - 150, self.screen.get_height() // 2 - 40), (50, 20)),
            text='-',
            manager=self.gui_manager,
            container=self.gui_manager.get_root_container(),
            object_id='no_border_button'
        )

        self.raise_volume_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screen.get_width() // 2 + 100, self.screen.get_height() // 2 - 40), (50, 20)),
            text='+',
            manager=self.gui_manager,
            container=self.gui_manager.get_root_container(),
            object_id='no_border_button'
        )

        self.add_button('Back', (self.screen.get_width() // 2 - 100, self.screen.get_height() // 2), self.back_action, 'no_border_button')

    def back_action(self):
        from Menu.MainMenu import MainMenu
        self.menu_manager.change_menu(MainMenu)

    def decrease_volume(self):
        if self.volume > 0:
            self.volume -= 10
            sound_manager.setMusicMenuVolume(self.volume/100)
            self.update_volume_display()

    def increase_volume(self):
        if self.volume < 100:
            self.volume += 10  # Збільшуємо гучність на 10 одиниць
            sound_manager.setMusicMenuVolume(self.volume/100)
            self.update_volume_display()

    def update_volume_display(self):
        self.volume_display.set_text(str(self.volume))  # Оновлюємо відображення поточного значення гучності

    def draw(self):
        super().draw()
        self.gui_manager.draw_ui(self.screen)

    def handle_event(self, event):
        super().handle_event(event)
        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.lower_volume_button:
                self.decrease_volume()
            elif event.ui_element == self.raise_volume_button:
                self.increase_volume()
