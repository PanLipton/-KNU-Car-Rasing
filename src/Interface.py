import pygame
import pygame_gui

class GameMenu:
    def __init__(self):
        pygame.init()

        self.WIDTH, self.HEIGHT = 1200, 800
        self.window_surface = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.manager = pygame_gui.UIManager((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()

        self.background = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.background.fill(pygame.Color('#000000'))

        self.state = 'main'
        self.volume = 1.0

        self.create_main_menu()
        self.create_settings_menu()

    def create_main_menu(self):
        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((350, 275), (100, 50)),
            text='Play',
            manager=self.manager)

        self.settings_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((350, 335), (100, 50)),
            text='Settings',
            manager=self.manager)

        self.exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((350, 395), (100, 50)),
            text='Exit',
            manager=self.manager)

    def create_settings_menu(self):
        self.volume_up_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((350, 275), (150, 50)),
            text='Volume Up',
            manager=self.manager,
            visible=False)

        self.volume_down_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((350, 335), (150, 50)),
            text='Volume Down',
            manager=self.manager,
            visible=False)

        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((350, 395), (100, 50)),
            text='Back',
            manager=self.manager,
            visible=False)

    def run(self):
        running = True
        while running:
            time_delta = self.clock.tick(60)/1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if self.state == 'main':
                        if event.ui_element == self.start_button:
                            print("Play the game")
                        elif event.ui_element == self.settings_button:
                            self.show_settings()
                        elif event.ui_element == self.exit_button:
                            running = False
                    elif self.state == 'settings':
                        if event.ui_element == self.volume_up_button:
                            self.change_volume(0.1)
                        elif event.ui_element == self.volume_down_button:
                            self.change_volume(-0.1)
                        elif event.ui_element == self.back_button:
                            self.show_main_menu()

                self.manager.process_events(event)

            self.manager.update(time_delta)

            self.window_surface.blit(self.background, (0, 0))
            self.manager.draw_ui(self.window_surface)

            pygame.display.update()

    def show_main_menu(self):
        self.state = 'main'
        self.start_button.show()
        self.settings_button.show()
        self.exit_button.show()
        self.volume_up_button.hide()
        self.volume_down_button.hide()
        self.back_button.hide()

    def show_settings(self):
        self.state = 'settings'
        self.start_button.hide()
        self.settings_button.hide()
        self.exit_button.hide()
        self.volume_up_button.show()
        self.volume_down_button.show()
        self.back_button.show()

    def change_volume(self, change):
        self.volume += change
        self.volume = min(max(self.volume, 0.0), 1.0)
        print(f"Volume: {self.volume}")

if __name__ == '__main__':
    game_menu = GameMenu()
    game_menu.run()
