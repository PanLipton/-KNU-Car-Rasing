import pygame
import sys
from GameController import GameController
from SoundManager.SoundManager import sound_manager


class GameOverScreen:
    _players = []
    def __init__(self, screen, game_over, players):
        self.screen = screen
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
        self.background_color = (0, 0, 0)
        #self.main_menu_text = self.font.render("Press SPACE to return to Main Menu", True, self.text_color_red)
        self.main_menu_text = pygame.font.Font('../assets/fonts/pixel_font.ttf', 48).render(
            "Press SPACE to return to Main Menu", True, (255, 255, 255))  # Увеличьте размер шрифта до 48


        #self.game_over_text = self.font_large.render("Game Over", True, self.text_color)
        #self.game_over_text_rect = self.game_over_text.get_rect(center=self.screen.get_rect().center)
        self.main_menu_text_rect = self.main_menu_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 115))

    def display_scores(self):
        players_dict = {}
        for i,player in enumerate(self._players):
            players_dict[player.get_score()] = score_text = self.font.render(f"Player {i + 1}: {player.get_score()}", True, self.text_color_red_black)

        sorted_dict = dict(sorted(players_dict.items(), key=lambda item: item[0], reverse=True))

        y_offset = 300  # Initial y offset
        for score, score_text in sorted_dict.items():
            score_text_rect = score_text.get_rect(center=(self.screen.get_width() // 2, y_offset))
            self.screen.blit(score_text, score_text_rect)

            # Increase y offset for next text
            y_offset += 50



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

            outline_text = pygame.font.Font('../assets/fonts/pixel_font.ttf', 48).render(
                "Press SPACE to return to Main Menu", True, (0, 0, 0))
            outline_text_rect = outline_text.get_rect(
                center=(self.screen.get_width() // 2 + 2, self.screen.get_height() // 2 + 52))  # Смещение на 2 пикселя

            self.main_menu_text_rect = self.main_menu_text.get_rect(
                center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 55))
            #self.screen.fill(self.background_color)
            self.screen.blit(self.game_over, (0, 0))  # Отображение заднего фона
            self.display_scores()
            #self.screen.blit(self.game_over_text, self.game_over_text_rect)
            self.screen.blit(outline_text, outline_text_rect)
            self.screen.blit(self.main_menu_text, self.main_menu_text_rect)

            pygame.display.flip()
