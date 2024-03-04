import pygame
import sys
from GameController import GameController
from src.SoundManager.SoundManager import sound_manager


class GameOverScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.font_large = pygame.font.Font(None, 72)
        self.text_color = (255, 255, 255)
        self.background_color = (0, 0, 0)
        self.main_menu_text = self.font.render("Press SPACE to return to Main Menu", True, self.text_color)
        self.game_over_text = self.font_large.render("Game Over", True, self.text_color)
        self.game_over_text_rect = self.game_over_text.get_rect(center=self.screen.get_rect().center)
        sound_manager.playSoundLose()
        self.main_menu_text_rect = self.main_menu_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 100))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_cont = GameController()
                        game_cont.run()

            self.screen.fill(self.background_color)
            self.screen.blit(self.game_over_text, self.game_over_text_rect)
            self.screen.blit(self.main_menu_text, self.main_menu_text_rect)
            pygame.display.flip()
