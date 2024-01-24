import pygame
import sys

# Инициализация pygame
pygame.init()

# Конфигурация экрана
WIDTH, HEIGHT = 1200, 800

# Опции меню
menu_items = ['Play', 'Settings', 'Exit']


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Terraria Menu')

    # Загрузка фонового изображения
    background = pygame.image.load('../img/backgroundimg1.jpg')
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    font = pygame.font.Font(None, 36)
    selected_item = 0

    while True:
        # Отображение фонового изображения
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and selected_item > 0:
                    selected_item -= 1
                elif event.key == pygame.K_DOWN and selected_item < len(menu_items) - 1:
                    selected_item += 1
                elif event.key == pygame.K_RETURN:
                    print(f"Вы выбрали {menu_items[selected_item]}")

        for index, item in enumerate(menu_items):
            color = (255, 255, 255)
            if index == selected_item:
                color = (255, 0, 0)

            label = font.render(item, True, color)
            screen.blit(label,
                        (WIDTH // 2 - label.get_width() // 2, HEIGHT // 2 - label.get_height() // 2 + index * 40))

        # Обновление дисплея
        pygame.display.flip()


if __name__ == "__main__":
    main()
