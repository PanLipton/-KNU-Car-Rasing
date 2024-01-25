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
    pygame.display.set_caption('Car Racing')

    # Загрузка фонового изображения
    background = pygame.image.load('../img/backgroundimg1.jpg')
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # Загрузка пиксельного шрифта
    title_font = pygame.font.Font('../fonts/pixel_font.ttf', 100)
    pixel_font = pygame.font.Font('../fonts/pixel_font.ttf', 36)

    selected_item = 0
    vertical_spacing = 60  # Интервал между кнопками

    while True:
        # Отображение фонового изображения
        screen.blit(background, (0, 0))

        title_label = title_font.render("Car Racing", True, (255, 255, 255))
        screen.blit(title_label,
                    (WIDTH // 2 - title_label.get_width() // 2, HEIGHT // 4 - title_label.get_height() // 2))

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
                    if menu_items[selected_item] == 'Exit':
                        pygame.quit()
                        sys.exit()
                    else:
                        print(f"Вы выбрали {menu_items[selected_item]}")
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 1 означает левую кнопку мыши
                    for index, item in enumerate(menu_items):
                        if (WIDTH // 2 - pixel_font.size(item)[0] // 2) < event.pos[0] < (WIDTH // 2 + pixel_font.size(item)[0] // 2) and \
                                (HEIGHT // 2 - pixel_font.size(item)[1] // 2 + index * vertical_spacing) < event.pos[1] < \
                                (HEIGHT // 2 - pixel_font.size(item)[1] // 2 + (index + 1) * vertical_spacing):
                            if item == 'Exit':
                                pygame.quit()
                                sys.exit()
                            else:
                                print(f"Вы выбрали {item}")

        for index, item in enumerate(menu_items):
            color = (255, 255, 255)

            # Получение координат курсора
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Проверка, находится ли курсор над текущей кнопкой
            if (WIDTH // 2 - pixel_font.size(item)[0] // 2) < mouse_x < (WIDTH // 2 + pixel_font.size(item)[0] // 2) and \
                    (HEIGHT // 2 - pixel_font.size(item)[1] // 2 + index * vertical_spacing) < mouse_y < \
                    (HEIGHT // 2 - pixel_font.size(item)[1] // 2 + (index + 1) * vertical_spacing):
                color = (255, 0, 0)  # Красный цвет при наведении

            label = pixel_font.render(item, True, color)
            screen.blit(label,
                        (WIDTH // 2 - label.get_width() // 2, HEIGHT // 2 - label.get_height() // 2 + index * vertical_spacing))

        # Обновление дисплея
        pygame.display.flip()


if __name__ == "__main__":
    main()
