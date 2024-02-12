import pygame
import pygame_gui
from menus.MainMenu import MainMenu
from MenuManager import MenuManager
from config import BACKGROUND_IMAGE_PATH 

class GameController:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1366, 900))
        pygame.display.set_caption('Car Racing')
        self.gui_manager = pygame_gui.UIManager((1366, 900), 'theme.json')
        self.menu_manager = MenuManager(self.screen, self.gui_manager)
        self.menu_manager.set_menu(MainMenu, BACKGROUND_IMAGE_PATH)  # Встановлення головного меню як початкового

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            time_delta = clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.USEREVENT:
                    self.menu_manager.handle_event(event)

                self.gui_manager.process_events(event)

            self.screen.fill((0, 0, 0))  # Очищення екрану
            self.menu_manager.draw()  # Малювання поточного меню
            self.gui_manager.update(time_delta)
            pygame.display.flip()

        pygame.quit()
