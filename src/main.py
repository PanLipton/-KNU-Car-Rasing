import pygame

from road import Road

# Встановлення параметрів екрану
screen_width = 1366
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))
# Словник з зображеннями доріг для різної кількості гравців
roads_images = {
    1: '../assets/img/road-5-lines.png',
    2: '../assets/img/road-6-lines.png',
}

# Умовна змінна кількості гравців
player_count = 2

# Вибір зображення дороги в залежності від кількості гравців
selected_road_image = roads_images.get(player_count, '../assets/img/road-5-lines.png')  

# Створення дороги
road1 = Road(selected_road_image, screen_width, screen_height)
road2 = Road(selected_road_image, screen_width, screen_height)
road2.rect.y = -road2.rect.height  # Початкова позиція другої дороги


# Основний цикл гри
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Оновлення позицій дороги
    road_speed = 0.65  # Швидкість 
    road1.update(road_speed)
    road2.update(road_speed)

    # Малювання дороги
    screen.blit(road1.image, road1.rect)
    screen.blit(road2.image, road2.rect)
    
    pygame.display.flip()