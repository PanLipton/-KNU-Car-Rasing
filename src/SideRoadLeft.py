import pygame


class SideRoadLeft(pygame.sprite.Sprite):
    def __init__(self, image_path, screen_width, screen_height):
        super().__init__()
        self.screen_height = screen_height
        self.screen_width = screen_width
        original_image = pygame.image.load(image_path).convert_alpha()
        self.y_offset = 0  # Додаткова змінна для збереження дробової частини зміщення

        # Ширина дороги - половина ширини екрану
        road_width = self.screen_width // 6
        # Зберегти оригінальне співвідношення сторін зображення
        aspect_ratio = original_image.get_height() / original_image.get_width()

        # Масштабируем изображение
        scaled_image = pygame.transform.scale(original_image, (road_width, self.screen_height))

        # Задаем начальное положение rect
        self.rect = scaled_image.get_rect(left=0, top=0)

        # Сохраняем изображение
        self.image = scaled_image

    def update(self, speed):
        self.y_offset += speed  # Додаємо дробову швидкість до дробової частини
        while self.y_offset >= 1:  # Якщо дробова частина більша або дорівнює 1
            self.rect.y += 1  # Рухаємо дорогу вниз на один піксель
            self.y_offset -= 1  # Віднімаємо 1 з дробової частини

        if self.rect.top >= self.screen_height:
            self.rect.y = -self.screen_height + int(self.y_offset)

    def get_edge_coordinates(self):
        # Повертає кортеж з лівої та правої координат X країв дороги.
        center_x = self.rect.centerx
        half_width = self.rect.width // 2
        left_edge = center_x - half_width
        right_edge = center_x + half_width
        return left_edge, right_edge