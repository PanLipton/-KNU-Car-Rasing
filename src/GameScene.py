# GameScene.py

import pygame
from Road.Road import Road
from Player.Player import APlayer


class GameScene:
    def __init__(self, screen, num_players):
        self.screen = screen
        self.num_players = num_players
        self.players = []  # Список гравців
        self.init_game()

    def init_game(self):
        # Ініціалізація дороги
        self.init_road()

    def init_road(self):
        # Припускаємо, що у вас є зображення дороги під назвою 'road.png' у папці 'assets/img'
        road_image_path = '../assets/img/road-6-lines.png'
        self.road1 = Road(road_image_path, self.screen.get_width(), self.screen.get_height())
        self.road2 = Road(road_image_path, self.screen.get_width(), self.screen.get_height())
        self.road2.rect.y = -self.road2.rect.height  # Початкова позиція для другої дороги
            

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.update()  # Оновлення логіки гри
            self.draw()  # Малювання сцени гри

            pygame.display.flip()  # Оновлення вмісту вікна на екрані

    def update(self):
        self.road1.update(5)
        self.road2.update(5)
        # Переміщення дороги назад вгору, коли вона повністю з'являється на екрані
        if self.road1.rect.top >= self.screen.get_height():
            self.road1.rect.y = -self.screen.get_height()
        if self.road2.rect.top >= self.screen.get_height():
            self.road2.rect.y = -self.screen.get_height()

    def draw(self):
        # Малювання дороги
        self.screen.blit(self.road1.image, self.road1.rect)
        self.screen.blit(self.road2.image, self.road2.rect)
