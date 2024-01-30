import pygame
import pygame_gui
import sys


class BaseMenu:
    def __init__(self, screen, title_font, pixel_font, background):
        self.screen = screen
        self.title_font = title_font
        self.pixel_font = pixel_font
        self.background = background
        self.gui_manager = pygame_gui.UIManager((screen.get_width(), screen.get_height()), 'theme.json')


class MainMenu(BaseMenu):
    def __init__(self, screen, title_font, pixel_font, background):
        super().__init__(screen, title_font, pixel_font, background)

        self.play_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screen.get_width() // 2 - 100, self.screen.get_height() // 2 - 40), (200, 30)),
            text='Play',
            manager=self.gui_manager,
            container=self.gui_manager.get_root_container(),
            object_id='no_border_button'
        )
        self.settings_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screen.get_width() // 2 - 100, self.screen.get_height() // 2), (200, 30)),
            text='Settings',
            manager=self.gui_manager,
            container=self.gui_manager.get_root_container(),
            object_id='no_border_button'
        )
        self.exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screen.get_width() // 2 - 100, self.screen.get_height() // 2 + 40), (200, 30)),
            text='Exit',
            manager=self.gui_manager,
            container=self.gui_manager.get_root_container(),
            object_id='no_border_button'
        )

    def handle_event(self, ui_element):
        if ui_element == self.play_button:
            print("Play button pressed")
        elif ui_element == self.settings_button:
            return SettingsMenu(self.screen, self.title_font, self.pixel_font, self.background)
        elif ui_element == self.exit_button:
            pygame.quit()
            sys.exit()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        title_label = self.title_font.render("Car Racing", True, (255, 255, 255))
        self.screen.blit(title_label, (self.screen.get_width() // 2 - title_label.get_width() // 2,
                                       self.screen.get_height() // 4 - title_label.get_height() // 2))
        self.gui_manager.draw_ui(self.screen)


class SettingsMenu(BaseMenu):
    def __init__(self, screen, title_font, pixel_font, background):
        super().__init__(screen, title_font, pixel_font, background)

        # Добавленные элементы
        self.volume_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.screen.get_width() // 2 - 100, self.screen.get_height() // 2 - 80), (200, 30)),
            text='Volume',
            manager=self.gui_manager,
            container=self.gui_manager.get_root_container(),
            object_id='no_border_label'  # Используем object_id для указания стиля
        )

        # self.volume_slider = pygame_gui.elements.UIHorizontalSlider(
        #     relative_rect=pygame.Rect((self.screen.get_width() // 2 - 100, self.screen.get_height() // 2 - 40), (200, 20)),
        #     start_value=50,
        #     value_range=(0, 100),
        #     manager=self.gui_manager,
        #     container=self.gui_manager.get_root_container(),
        #     object_id='no_border_button'
        # )

        # Добавляем кнопки Volume Up и Volume Down
        self.volume_up_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screen.get_width() // 2 - 100, self.screen.get_height() // 2 - 40),
                                      (200, 30)),
            text='Volume Up',
            manager=self.gui_manager,
            container=self.gui_manager.get_root_container(),
            object_id='no_border_button'
        )

        self.volume_down_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screen.get_width() // 2 - 100, self.screen.get_height() // 2), (200, 30)),
            text='Volume Down',
            manager=self.gui_manager,
            container=self.gui_manager.get_root_container(),
            object_id='no_border_button'
        )

        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screen.get_width() // 2 - 100, self.screen.get_height() // 2 + 40),
                                      (200, 30)),
            text='Back',
            manager=self.gui_manager,
            container=self.gui_manager.get_root_container(),
            object_id='no_border_button'
        )

    def handle_event(self, ui_element):
        if ui_element == self.back_button:
            return MainMenu(self.screen, self.title_font, self.pixel_font, self.background)
        elif ui_element == self.volume_up_button:
            # Обработка увеличения громкости
            print("Volume Up button pressed")
        elif ui_element == self.volume_down_button:
            # Обработка уменьшения громкости
            print("Volume Down button pressed")

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        title_label = self.title_font.render("Settings", True, (255, 255, 255))
        self.screen.blit(title_label, (self.screen.get_width() // 2 - title_label.get_width() // 2,
                                       self.screen.get_height() // 4 - title_label.get_height() // 2))
        self.gui_manager.draw_ui(self.screen)


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
        background = pygame.image.load('../../assets/img/backgroundimg.jpg')
        self.background = pygame.transform.scale(background, (self.WIDTH, self.HEIGHT))

        # Загрузка пиксельного шрифта
        self.title_font = pygame.font.Font('../../assets/fonts/pixel_font.ttf', 100)
        self.pixel_font = pygame.font.Font('../../assets/fonts/pixel_font.ttf', 20)  # Изменение размера для надписи "Volume"

        self.current_menu = MainMenu(self.screen, self.title_font, self.pixel_font, self.background)

    def run(self):
        clock = pygame.time.Clock()
        is_running = True

        while is_running:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                if event.type == pygame.USEREVENT:
                    if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        new_menu = self.current_menu.handle_event(event.ui_element)
                        if new_menu:
                            self.current_menu = new_menu

                self.current_menu.gui_manager.process_events(event)

            self.current_menu.draw()
            self.current_menu.gui_manager.update(time_delta)

            pygame.display.flip()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Menu().run()
