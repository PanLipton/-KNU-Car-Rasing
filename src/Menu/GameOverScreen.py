import pygame
import sys
from GameController import GameController
from SoundManager.SoundManager import sound_manager

class GameOverScreen:
    _players = []
    def __init__(self, screen, game_over, players):
        self.screen = screen
<<<<<<< HEAD:src/GameOverScreen.py
        self.game_over = pygame.image.load("../assets/img/gameoverimg.jpg").convert()
        self.game_over = pygame.transform.scale(self.game_over, (
        screen.get_width(), screen.get_height()))  # Масштабирование изображения
        self._players = players
        self.font = pygame.font.Font(None, 36)
        self.font_large = pygame.font.Font(None, 72)
        #title_font = pygame.font.Font(('../assets/fonts/pixel_font.ttf'), 100)
        pixel_font_path = "../assets/fonts/pixel_font.ttf"

        self.font = pygame.font.Font(pixel_font_path, 30)  # Используйте пиксельный шрифт для маленького текста
        self.font_large = pygame.font.Font(pixel_font_path, 48)  # Используйте пиксе
        #self.text_color_red = (0, 0, 102)
        self.text_color_red_black = (0, 0, 0)
=======
        self.background_image = pygame.image.load(background_image_path).convert()
        self.background_image = pygame.transform.scale(self.background_image, (screen.get_width(), screen.get_height()))  # Масштабування зображення
        self._players = players
        self.font = pygame.font.Font(None, 36)
        self.font_large = pygame.font.Font(None, 72)
        self.text_color = (255, 255, 255)
>>>>>>> 3fbfe50bdaa59de8fecca17d7c71352ebe922b46:src/Menu/GameOverScreen.py
        self.background_color = (0, 0, 0)
        #self.main_menu_text = self.font.render("Press SPACE to return to Main Menu", True, self.text_color_red)
        self.main_menu_text = pygame.font.Font('../assets/fonts/pixel_font.ttf', 48).render(
            "Press SPACE to return to Main Menu", True, (255, 255, 255))  # Увеличьте размер шрифта до 48


        #self.game_over_text = self.font_large.render("Game Over", True, self.text_color)
        #self.game_over_text_rect = self.game_over_text.get_rect(center=self.screen.get_rect().center)
        self.main_menu_text_rect = self.main_menu_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 115))

        self.max_score = self.load_max_score()

    def display_scores(self):
<<<<<<< HEAD:src/GameOverScreen.py
        players_dict = {}
        for i,player in enumerate(self._players):
            players_dict[player.get_score()] = score_text = self.font.render(f"Player {i + 1}: {player.get_score()}", True, self.text_color_red_black)

        sorted_dict = dict(sorted(players_dict.items(), key=lambda item: item[0], reverse=True))

        y_offset = 300  # Initial y offset
        for score, score_text in sorted_dict.items():
            score_text_rect = score_text.get_rect(center=(self.screen.get_width() // 2, y_offset))
=======
        highest_score = 0
        for i, player in enumerate(self._players):
            score = player.get_score()
            highest_score = max(highest_score, score)
            score_text = self.font.render(f"Player {i + 1}: {score}", True, self.text_color)
            score_text_rect = score_text.get_rect(center=(self.screen.get_width() // 2, 50 + i * 50))
>>>>>>> 3fbfe50bdaa59de8fecca17d7c71352ebe922b46:src/Menu/GameOverScreen.py
            self.screen.blit(score_text, score_text_rect)

        if highest_score > self.max_score:
            self.save_max_score(highest_score)
            self.max_score = highest_score  # Оновлення max_score для відображення

        max_score_text = self.font.render(f"Max Score: {self.max_score}", True, self.text_color)
        max_score_rect = max_score_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 150))
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

<<<<<<< HEAD:src/GameOverScreen.py
            outline_text = pygame.font.Font('../assets/fonts/pixel_font.ttf', 48).render(
                "Press SPACE to return to Main Menu", True, (0, 0, 0))
            outline_text_rect = outline_text.get_rect(
                center=(self.screen.get_width() // 2 + 2, self.screen.get_height() // 2 + 52))  # Смещение на 2 пикселя

            self.main_menu_text_rect = self.main_menu_text.get_rect(
                center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 55))
            #self.screen.fill(self.background_color)
            self.screen.blit(self.game_over, (0, 0))  # Отображение заднего фона
=======
            self.screen.blit(self.background_image, (0, 0))  # Відображення заднього фону
>>>>>>> 3fbfe50bdaa59de8fecca17d7c71352ebe922b46:src/Menu/GameOverScreen.py
            self.display_scores()
            #self.screen.blit(self.game_over_text, self.game_over_text_rect)
            self.screen.blit(outline_text, outline_text_rect)
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
