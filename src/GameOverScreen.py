import pygame
import sys
from GameController import GameController
from SoundManager.SoundManager import sound_manager


class GameOverScreen:
    def __init__(self, screen, background_image_path, players):
        self.screen = screen
        self.background_image = pygame.image.load(background_image_path).convert()
        self.background_image = pygame.transform.scale(self.background_image, (
        screen.get_width(), screen.get_height()))  # Масштабирование изображения
        self.players = players
        self.font = pygame.font.Font(None, 36)
        self.font_large = pygame.font.Font(None, 72)
        title_font = pygame.font.Font(('../assets/fonts/pixel_font.ttf'), 100)
        self.text_color = (255, 255, 255)
        self.background_color = (0, 0, 0)
        self.main_menu_text = self.font.render("Press SPACE to return to Main Menu", True, self.text_color)
        self.game_over_text = self.font_large.render("Game Over", True, self.text_color)
        self.game_over_text_rect = self.game_over_text.get_rect(center=self.screen.get_rect().center)
        sound_manager.playSoundLose()
        self.main_menu_text_rect = self.main_menu_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 100))

    def display_scores(self):
        sorted_players = sorted(self.players, key=lambda player: player.get_score(), reverse=True)
        y_offset = 100
        for i, player in enumerate(sorted_players):
            score_text = self.font.render(f"Player {i + 1}: {player.get_score()}", True, self.text_color)
            score_text_rect = score_text.get_rect(center=(self.screen.get_width() // 2, y_offset))
            self.screen.blit(score_text, score_text_rect)
            y_offset += 50

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

            #self.screen.fill(self.background_color)
            self.screen.blit(self.background_image, (0, 0))  # Отображение заднего фона
            self.display_scores()
            self.screen.blit(self.game_over_text, self.game_over_text_rect)
            self.screen.blit(self.main_menu_text, self.main_menu_text_rect)

            pygame.display.flip()