# GameScene.py

import pygame
from Road.Road import Road
from Player.Player import APlayer
import random
from Bot.Bot import Bot
from pathlib import Path

class GameScene:
    def __init__(self, screen, num_players):
        self.screen = screen
        self.num_players = num_players
        self.players = []  # Список гравців
        self.obstacles = pygame.sprite.Group()
        self.spawn_delay = 175  # Початкова затримка спавну ботів в мілісекундах
        self.bot_speed = 1  # Початкова швидкість ботів
        self.last_spawn_time = pygame.time.get_ticks()  # Останній час спавну
        self.difficulty_increase_interval = 30000  # Інтервал збільшення складності (30 секунд)
        self.last_difficulty_increase_time = pygame.time.get_ticks()  # Останнє збільшення складності
        self.score_update_interval = 1000 # Очки нараховуються кожну секунду
        self.last_score_update_time = pygame.time.get_ticks()

        self.init_game()

    def init_game(self):
        # Ініціалізація дороги
        self.init_road()
        self.init_players()


    def init_road(self):
        road_image_path = Path('../assets/img/road-6-lines.png')
        self.road1 = Road(road_image_path, self.screen.get_width(), self.screen.get_height())
        self.road2 = Road(road_image_path, self.screen.get_width(), self.screen.get_height())
        self.road2.rect.y = -self.road2.rect.height  # Початкова позиція для другої дороги
        

    def init_players(self):
        x_position = [289.3, 584.7, 1034.1]
        for i in range(self.num_players):
            player_image_path = Path(f'../assets/cars/player-car-{i+1}.png')
            player = APlayer(self.screen, player_image_path, x_position[i], 500, 70, 118)
            self.players.append(player)

    def update_scores(self):
        for player in self.players:
            player._change_score(1)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.update()  # Оновлення логіки гри
            self.draw()  # Малювання сцени гри

            pygame.display.flip()  # Оновлення вмісту вікна на екрані

    def spawn_bot(self):
        bot_model = random.choice(["bot-1.png", "bot-2.png", "bot-3.png", "bot-4.png", "bot-5.png", "bot-6.png"])
        random_lines_coordinates = [289.3, 432.79, 584.7, 736.6, 889.9, 1034.1]
        
        for _ in range(10):  # Обмежуємо кількість спроб
            # Вибір випадкової позиції
            start_x = random.choice(random_lines_coordinates) + random.choice([-1, 1]) * random.randrange(1, 5)
            
            # Створення тимчасового rect для перевірки перекриття
            temp_rect = pygame.Rect(start_x, -118, 70, 118)
            
            # Перевірка на перекриття з існуючими ботами
            collision = any(temp_rect.colliderect(bot.rect) for bot in self.obstacles)
            
            if not collision:
                new_bot = Bot(self.screen, bot_model, start_x, -118, 70, 118)
                self.obstacles.add(new_bot)
                break
        


    def update(self):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        self.update_scores()
        if current_time - self.last_difficulty_increase_time > self.difficulty_increase_interval:
            self.bot_speed += 0.2  # Збільшуйте швидкість ботів
            self.spawn_delay = max(80, self.spawn_delay - 7)  # Зменшуйте затримку спавну, але не менше 200 мс
            self.last_difficulty_increase_time = current_time
        left_edge, right_edge = self.road1.get_edge_coordinates()
        
        if current_time - self.last_spawn_time > self.spawn_delay:
            self.spawn_bot()
            self.last_spawn_time = current_time     
        # Керування для гравця 1
        if self.num_players >= 1:
            if keys[pygame.K_w]: self.players[0].MoveUP(0.7, self.obstacles)
            if keys[pygame.K_s]: self.players[0].MoveDown(0.7, self.obstacles)
            if keys[pygame.K_a]: self.players[0].MoveLeft(0.7, self.obstacles, left_edge)
            if keys[pygame.K_d]: self.players[0].MoveRight(0.7, self.obstacles, right_edge)
        if self.num_players >= 2:
            if keys[pygame.K_y]: self.players[1].MoveUP(0.7, self.obstacles)
            if keys[pygame.K_h]: self.players[1].MoveDown(0.7, self.obstacles)
            if keys[pygame.K_g]: self.players[1].MoveLeft(0.7, self.obstacles, left_edge)
            if keys[pygame.K_j]: self.players[1].MoveRight(0.7, self.obstacles, right_edge)
        if self.num_players >= 3:
            if keys[pygame.K_UP]: self.players[2].MoveUP(0.7, self.obstacles)
            if keys[pygame.K_DOWN]: self.players[2].MoveDown(0.7, self.obstacles)
            if keys[pygame.K_LEFT]: self.players[2].MoveLeft(0.7, self.obstacles, left_edge)
            if keys[pygame.K_RIGHT]: self.players[2].MoveRight(0.7, self.obstacles, right_edge)
        
        for bot in list(self.obstacles):  # Використовуйте list() для копіювання, щоб уникнути помилок під час ітерації
            bot.MoveDown(self.bot_speed)
            if bot.getActorLocation()[1] > 900:  # Перевірка чи бот вийшов за межі екрану
                self.obstacles.remove(bot)  # Видалення бота з групи перешкод

        roadspeed = 0.7
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
        for bot in self.obstacles:
            bot.draw()
        for player in self.players:
            player.draw()