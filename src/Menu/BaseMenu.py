# BaseMenu.py

import pygame
import pygame_gui
from SoundManager.SoundManager import sound_manager

class BaseMenu:
    def __init__(self, screen, gui_manager, menu_manager, background_image_path, title_text="", title_font=None, title_color=(255, 255, 255)):
        self.screen = screen
        self.gui_manager = gui_manager
        self.menu_manager = menu_manager
        self.background = self.load_background_image(background_image_path, screen.get_size())
        self.title_text = title_text
        self.title_font = title_font if title_font else pygame.font.Font(None, 36)  # Використовуємо заданий шрифт або стандартний
        self.title_color = title_color
        self.buttons = []
        self.play_background_music()
        
    def add_button(self, text, position, action=None, object_id=None):
        button_style = object_id if object_id else 'default_button'
        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(position, (200, 30)),
            text=text,
            manager=self.gui_manager,
            container=self.gui_manager.get_root_container(),
            object_id=button_style
        )
        self.buttons.append((button, action))

    def play_background_music(self):
        pygame.mixer.music.load('../assets/music/musicMenu.mp3')
        #pygame.mixer.music.set_volume(self.__volume)  # Начальная громкость
        pygame.mixer.music.play(-1)

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)

    def handle_event(self, event):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                sound_manager.playSoundButton()
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
        if self.background:
            self.screen.blit(self.background, (0, 0))
        if self.title_text:
            title_label = self.title_font.render(self.title_text, True, self.title_color)
            self.screen.blit(title_label, (self.screen.get_width() // 2 - title_label.get_width() // 2,
                                           self.screen.get_height() // 4 - title_label.get_height() // 2))
        self.gui_manager.draw_ui(self.screen)
