import pygame
import sys
from GameController import GameController
from SoundManager.SoundManager import sound_manager

class GameOverScreen:
    _players = []
    def __init__(self, screen, game_over, players):
        self.screen = screen
        self.game_over = pygame.image.load("../assets/img/gameoverimg.jpg").convert()
        self.game_over = pygame.transform.scale(self.game_over, (screen.get_width(), screen.get_height()))  # Масштабування зображення
        self._players = players
        self.font = pygame.font.Font(None, 36)
        self.font_large = pygame.font.Font(None, 72)
        pixel_font_path = "../assets/fonts/pixel_font.ttf"
        self.font = pygame.font.Font(pixel_font_path, 30)  # Використовуйте піксельний шрифт для маленького тексту
        self.font_large = pygame.font.Font(pixel_font_path, 48)  # Використовуйте піксельний шрифт для великого тексту
        self.text_color_red_black = (0, 0, 0)
        self.background_color = (0, 0, 0)
        self.main_menu_text = pygame.font.Font(pixel_font_path, 48).render("Press SPACE to return to Main Menu", True, (255, 255, 255))
        self.main_menu_text_rect = self.main_menu_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 115))
        
        # Завантаження максимального рахунку
        self.max_score = self.load_max_score()

    def display_scores(self):
        highest_score = 0
        for i, player in enumerate(self._players):
            score = player.get_score()
            highest_score = max(highest_score, score)
            score_text = self.font.render(f"Player {i + 1}: {score}", True, self.text_color_red_black)
            score_text_rect = score_text.get_rect(center=(self.screen.get_width() // 2, 300 + i * 50))
            self.screen.blit(score_text, score_text_rect)

        # Оновлення та збереження максимального рахунку, якщо потрібно
        if highest_score > self.max_score:
            self.save_max_score(highest_score)
            self.max_score = highest_score

        max_score_text = self.font.render(f"Max Score: {self.max_score}", True, self.text_color_red_black)
        max_score_rect = max_score_text.get_rect(center=(self.screen.get_width() // 2, 250))
        self.screen.blit(max_score_text, max_score_rect)

    def run(self):
        sound_manager.playSoundLose()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_cont = GameController()
                        game_cont.run()

            self.screen.blit(self.game_over, (0, 0))  # Відображення заднього фону
            self.display_scores()
            self.screen.blit(self.main_menu_text, self.main_menu_text_rect)
            pygame.display.flip()

    def load_max_score(self):
        try:
            with open('max_score.txt', 'r') as file:
                return int(file.read())
        except FileNotFoundError:
            return 0

    def save_max_score(self, score):
        with open('max_score.txt', 'w') as file:
            file.write(str(score))

