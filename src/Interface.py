import pygame
import pygame_gui
import sys

class Menu:
    def __init__(self):
        pygame.init()

        # Конфигурация экрана
        self.WIDTH, self.HEIGHT = 1200, 800

        # Опции меню
        self.menu_items = ['Play', 'Settings', 'Exit']

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Car Racing')

        # Загрузка фонового изображения
        self.background = pygame.image.load('../assets/img/backgroundimg.jpg')
        self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))

        # Загрузка пиксельного шрифта
        self.title_font = pygame.font.Font('../fonts/pixel_font.ttf', 100)
        self.pixel_font = pygame.font.Font('../fonts/pixel_font.ttf', 36)
        self.gui_manager = pygame_gui.UIManager((self.WIDTH, self.HEIGHT), '../src/theme.json')

        # Опции главного меню
        self.play_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.WIDTH // 2 - 100, self.HEIGHT // 2 - 40), (200, 30)),
                                                         text='Play',
                                                         manager=self.gui_manager,
                                                         container=self.gui_manager.get_root_container(),
                                                         object_id='no_border_button')
        self.settings_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.WIDTH // 2 - 100, self.HEIGHT // 2), (200, 30)),
                                                             text='Settings',
                                                             manager=self.gui_manager,
                                                             container=self.gui_manager.get_root_container(),
                                                             object_id='no_border_button')
        self.exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.WIDTH // 2 - 100, self.HEIGHT // 2 + 40), (200, 30)),
                                                         text='Exit',
                                                         manager=self.gui_manager,
                                                         container=self.gui_manager.get_root_container(),
                                                         object_id='no_border_button')

        # Опции меню настроек
        self.volume_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((self.WIDTH // 2 - 100, self.HEIGHT // 2 - 40), (200, 20)),
                                                                    start_value=50,
                                                                    value_range=(0, 100),
                                                                    manager=self.gui_manager,
                                                                    visible=0,
                                                                    container=self.gui_manager.get_root_container(),
                                                                    object_id='no_border_button')
        self.back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.WIDTH // 2 - 100, self.HEIGHT // 2), (200, 30)),
                                                        text='Back',
                                                        manager=self.gui_manager,
                                                        visible=0,
                                                        container=self.gui_manager.get_root_container(),
                                                        object_id='no_border_button')

        self.selected_item = 0
        self.vertical_spacing = 60  # Интервал между кнопками

    def run(self):
        clock = pygame.time.Clock()
        is_running = True
        settings = False
        while is_running:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.play_button:
                            print("Play button pressed")
                        elif event.ui_element == self.settings_button:
                            settings = True
                            self.play_button.hide()
                            self.settings_button.hide()
                            self.exit_button.hide()
                            self.volume_slider.show()
                            self.back_button.show()
                        elif event.ui_element == self.exit_button:
                            is_running = False
                        elif event.ui_element == self.back_button:
                            settings = False
                            self.play_button.show()
                            self.settings_button.show()
                            self.exit_button.show()
                            self.volume_slider.hide()
                            self.back_button.hide()
                self.gui_manager.process_events(event)
            self.screen.blit(self.background, (0, 0))
            title_label = self.title_font.render("Car Racing", True, (255, 255, 255))
            self.screen.blit(title_label, (self.WIDTH // 2 - title_label.get_width() // 2, self.HEIGHT // 4 - title_label.get_height() // 2))
            self.gui_manager.update(time_delta)
            self.gui_manager.draw_ui(self.screen)
            pygame.display.flip()
        pygame.quit()
        sys.exit()
if __name__ == "__main__":
    Menu().run()
