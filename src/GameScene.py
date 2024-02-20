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
        self.init_players()


    def init_road(self):
        road_image_path = '../assets/img/road-6-lines.png'
        self.road1 = Road(road_image_path, self.screen.get_width(), self.screen.get_height())
        self.road2 = Road(road_image_path, self.screen.get_width(), self.screen.get_height())
        self.road2.rect.y = -self.road2.rect.height  # Початкова позиція для другої дороги
        

    def init_players(self):
        player_image_path = '../assets/cars/player-car-1.png'
        player = APlayer(self.screen, player_image_path, 430, 500, 50, 100)
        self.players.append(player)

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
        keys = pygame.key.get_pressed()

        # Якщо наразі немає перешкод, створіть порожній список
        obstacles = []
        # Керування для гравця 1
        if self.num_players >= 1:
            if keys[pygame.K_w]: self.players[0].MoveUP(0.7, obstacles)
            if keys[pygame.K_s]: self.players[0].MoveDown(0.7, obstacles)
            if keys[pygame.K_a]: self.players[0].MoveLeft(0.7, obstacles)
            if keys[pygame.K_d]: self.players[0].MoveRight(0.7, obstacles)


        roadspeed = 0.65
        self.road1.update(roadspeed)
        self.road2.update(roadspeed)
        # Переміщення дороги назад вгору, коли вона повністю з'являється на екрані
        if self.road1.rect.top >= self.screen.get_height():
            self.road1.rect.y = -self.screen.get_height()
        if self.road2.rect.top >= self.screen.get_height():
            self.road2.rect.y = -self.screen.get_height()

    def draw(self):
        # Малювання дороги
        self.screen.blit(self.road1.image, self.road1.rect)
        self.screen.blit(self.road2.image, self.road2.rect)
        for player in self.players:
            player.draw()
