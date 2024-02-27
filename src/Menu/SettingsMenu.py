import pygame
import pygame_gui
from Menu.BaseMenu import BaseMenu
from src.SoundManager.SoundManager import sound_manager


class SettingsMenu(BaseMenu):
    def __init__(self, screen, gui_manager, menu_manager, background_image_path):
        title_font = pygame.font.Font('../assets/fonts/pixel_font.ttf', 100)
        super().__init__(screen, gui_manager, menu_manager, background_image_path, "Car Racing", title_font)
        self.slider_position = 0.5  # Значення за замовчуванням
        self.create_ui_elements()

    def create_ui_elements(self):
        self.volume_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.screen.get_width() // 2 - 100, self.screen.get_height() // 2 - 120), (200, 30)),
            text='Volume',
            manager=self.gui_manager,
            container=self.gui_manager.get_root_container(),
            object_id='no_border_label'
        )

        slider_width = 200
        slider_height = 20
        slider_x = (self.screen.get_width() - slider_width) // 2
        slider_y = self.screen.get_height() // 2 - slider_height // 2 - 20  # Змінено положення по Y

        self.volume_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((slider_x, slider_y), (slider_width, slider_height)),
            start_value=self.slider_position,
            value_range=(0.0, 1.0),
            manager=self.gui_manager,
            container=self.gui_manager.get_root_container()
        )

        self.add_button('Back', (self.screen.get_width() // 2 - 100, self.screen.get_height() // 2), self.back_action, 'no_border_button')

    def back_action(self):
        from Menu.MainMenu import MainMenu
        self.slider_position = self.volume_slider.get_current_value()  # Зберігаємо поточне положення повзунка
        self.menu_manager.change_menu(MainMenu)

    def update_volume(self):
        volume = int(self.volume_slider.get_current_value() * 100)
        sound_manager.setMusicMenuVolume(volume / 100)

    def draw(self):
        super().draw()
        self.gui_manager.draw_ui(self.screen)

    def handle_event(self, event):
        super().handle_event(event)
        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            self.update_volume()
