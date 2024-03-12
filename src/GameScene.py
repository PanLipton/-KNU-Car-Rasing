# GameScene.py
import struct
import pygame
from Road.Road import Road
from Player.Player import APlayer
from Collision.Collision import UBoxCollision
import random
from Bot.Bot import Bot
from pathlib import Path
from GameRenderer import GameRenderer
from Menu.GameOverScreen import GameOverScreen
from SoundManager.SoundManager import sound_manager


class GameScene:
    _obstacles = []

    def __init__(self, screen, num_players):
        self.screen = screen
        self.num_players = num_players
        self.players = []  # Список гравців
        self.gameover = GameOverScreen(self.screen, '../assets/img/backgroundimg.jpg', self.players)
        self.obstacles = pygame.sprite.Group()

        self.spawn_delay = 3000  # Початкова затримка спавну ботів в мілісекундах
        self.bot_speed = 1  # Початкова швидкість ботів
        self.last_spawn_time = pygame.time.get_ticks()  # Останній час спавну
        self.difficulty_increase_interval = 1000  # Інтервал збільшення складності (30 секунд)
        self.last_difficulty_increase_time = pygame.time.get_ticks()  # Останнє збільшення складності

        self.isGameEnded = False
        self.clock = pygame.time.Clock()
        self.renderer = GameRenderer(screen)
        self.init_game()

    def init_game(self):
        with open("../assets/bin/volume.bin", "rb") as f:
            data = f.read(4)
            float_value = struct.unpack("f", data)[0]

            sound_manager.setMusicVolume(float_value)

        sound_manager.playMusicGame()

        self.init_road()
        self.init_road_collision()
        self.init_players()

    def init_road_collision(self):
        self._obstacles.append(UBoxCollision(self.screen, 100, 0, self.screen.get_width()-100, 1, 'Orange')) # Верхня сторона
        self._obstacles.append(UBoxCollision(self.screen, 100, self.screen.get_height(), self.screen.get_width()-100, 1, 'Orange')) # Нижня сторона
        self._obstacles.append(UBoxCollision(self.screen, 0, 0, 240, self.screen.get_height(), 'Orange')) # Ліва сторона
        self._obstacles.append(UBoxCollision(self.screen, self.screen.get_width() - 240, 0, 240, self.screen.get_height(), 'Orange')) # Права сторона


    def init_road(self):
        road_image_path = Path('../assets/img/road-6-lines.png')
        self.road1 = Road(road_image_path, self.screen.get_width(), self.screen.get_height())
        self.road2 = Road(road_image_path, self.screen.get_width(), self.screen.get_height())
        self.road2.rect.y = -self.road2.rect.height  # Початкова позиція для другої дороги

    def init_players(self):
        x_position = [289.3, 584.7, 1034.1]
        for i in range(self.num_players):
            player_image_path = Path(f'../assets/cars/player-car-{i + 1}.png')
            player = APlayer(self.screen, player_image_path, x_position[i], 500, 70, 118)
            self.players.append(player)

    def update_scores(self):
        for player in self.players:
            if player.is_active:
                player.change_score(1)


    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.update()  # Оновлення логіки гри
            self.draw()  # Малювання сцени гри
            self.clock.tick(300)
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

    def check_game_end(self):
        if all(not player.is_active for player in self.players):
            self.gameover.run() 

    def update(self):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        self.update_scores()

        if current_time - self.last_difficulty_increase_time > self.difficulty_increase_interval:
            self.bot_speed += 0.005  # Збільшення швидкісті ботів
            self.spawn_delay = max(350, self.spawn_delay - 75)  # Зменшення затримки спавну, але не менше 350 мс
            self.last_difficulty_increase_time = current_time
        left_edge, right_edge = self.road1.get_edge_coordinates()

        if current_time - self.last_spawn_time > self.spawn_delay:
            self.spawn_bot()

            self.last_spawn_time = current_time
            # Керування для гравців

            self.last_spawn_time = current_time
            # Керування для гравця 1

        if self.num_players >= 1:
            if keys[pygame.K_w]: self.players[0].MoveUP(0.7, self._obstacles)
            if keys[pygame.K_s]: self.players[0].MoveDown(0.7, self._obstacles)
            if keys[pygame.K_a]: self.players[0].MoveLeft(0.7, self._obstacles)
            if keys[pygame.K_d]: self.players[0].MoveRight(0.7, self._obstacles)
        if self.num_players >= 2:
            if keys[pygame.K_y]: self.players[1].MoveUP(0.7, self._obstacles)
            if keys[pygame.K_h]: self.players[1].MoveDown(0.7, self._obstacles)
            if keys[pygame.K_g]: self.players[1].MoveLeft(0.7, self._obstacles)
            if keys[pygame.K_j]: self.players[1].MoveRight(0.7, self._obstacles)
        if self.num_players >= 3:
            if keys[pygame.K_UP]: self.players[2].MoveUP(0.7, self._obstacles)
            if keys[pygame.K_DOWN]: self.players[2].MoveDown(0.7, self._obstacles)
            if keys[pygame.K_LEFT]: self.players[2].MoveLeft(0.7, self._obstacles)
            if keys[pygame.K_RIGHT]: self.players[2].MoveRight(0.7, self._obstacles)

        for bot in list(self.obstacles):  # Використовуйте list() для копіювання, щоб уникнути помилок під час ітерації
            bot.MoveDown(self.bot_speed)
            if bot.getActorLocation()[1] > 900:  # Перевірка чи бот вийшов за межі екрану
                self.obstacles.remove(bot)  # Видалення бота з групи перешкод
        players_group = pygame.sprite.Group(self.players)
        all_sprites = pygame.sprite.Group()
        all_sprites.add(players_group, self.obstacles)
        roadspeed = 1.7
        self.road1.update(roadspeed)
        self.road2.update(roadspeed)
        # Переміщення дороги назад вгору, коли вона повністю з'являється на екрані
        if self.road1.rect.top >= self.screen.get_height():
            self.road1.rect.y = -self.screen.get_height()
        if self.road2.rect.top >= self.screen.get_height():
            self.road2.rect.y = -self.screen.get_height()

        for player in self.players:
            # Перевірка на зіткнення для кожного гравця
            if player.is_active:  # Перевірка, чи активний гравець
                player.update(all_sprites)  # Оновлення активного гравця
        self.check_game_end()

    def draw(self):
        # Відмальовуємо дорогу
        self.renderer.draw_road(self.road1, self.road2)
        # Відмальовуємо колізію
        for obstacle in self._obstacles:
            obstacle.draw()
        # Відмальовуємо гравців
        self.renderer.draw_players(self.players)
        # Відмальовуємо анімацію вибуху для кожного гравця, якщо вона активна
        self.renderer.draw_explosions(self.players)
        # Відмальовуємо інші елементи гри
        self.renderer.draw_bots(self.obstacles)




