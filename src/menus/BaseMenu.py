# BaseMenu.py

import pygame
import pygame_gui
class BaseMenu:
    def __init__(self, screen, gui_manager, menu_manager, background_image_path):
        self.screen = screen
        self.gui_manager = gui_manager
        self.menu_manager = menu_manager
        self.background = self.load_background_image(background_image_path, screen.get_size())
        self.buttons = []

    def add_button(self, text, position, action=None):
        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(position, (200, 30)),
            text=text,
            manager=self.gui_manager
        )
        self.buttons.append((button, action))

    def handle_event(self, event):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                for button, action in self.buttons:
                    if event.ui_element == button:
                        action()

    def load_background_image(self, image_path, size):
        # Завантаження зображення та адаптація його розміру до вказаного
        try:
            background = pygame.image.load(image_path)
            background = pygame.transform.scale(background, size)
            return background
        except pygame.error as e:
            print(f"Error loading background image: {e}")
            return None

    def draw_background(self):
        if self.background:
            self.screen.blit(self.background, (0, 0))

    def draw(self):
        # Метод для перевизначення в нащадках
        self.draw_background()
