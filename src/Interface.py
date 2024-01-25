import pygame
import sys

class Menu:
    def __init__(self):
        # Инициализация pygame
        pygame.init()

        # Инициализация микшера pygame
        pygame.mixer.init()

        # Конфигурация экрана
        self.WIDTH, self.HEIGHT = 1200, 800

        # Опции меню
        self.menu_items = ['Play', 'Settings', 'Exit']
        self.settings_items = ['Volume Up', 'Volume Down', 'Back']

        # Текущее состояние меню
        self.state = 'main'

        # Громкость звука
        self.volume = 1.0

    def change_volume(self, change):
        self.volume += change
        self.volume = min(max(self.volume, 0.0), 1.0)  # Ограничиваем громкость от 0.0 до 1.0
        pygame.mixer.music.set_volume(self.volume)

    def main(self):
        screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Car Racing')

        # Загрузка фонового изображения
        background = pygame.image.load('../img/backgroundimg1.jpg')
        background = pygame.transform.scale(background, (self.WIDTH, self.HEIGHT))

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
                        (self.WIDTH // 2 - title_label.get_width() // 2, self.HEIGHT // 4 - title_label.get_height() // 2))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and selected_item > 0:
                        selected_item -= 1
                    elif event.key == pygame.K_DOWN and selected_item < len(self.menu_items) - 1:
                        selected_item += 1
                    elif event.key == pygame.K_RETURN:
                        if self.state == 'main':
                            if self.menu_items[selected_item] == 'Exit':
                                pygame.quit()
                                sys.exit()
                            elif self.menu_items[selected_item] == 'Settings':
                                self.state = 'settings'
                                selected_item = 0
                            else:
                                print(f"Вы выбрали {self.menu_items[selected_item]}")
                        elif self.state == 'settings':
                            if self.settings_items[selected_item] == 'Back':
                                self.state = 'main'
                                selected_item = 0
                            elif self.settings_items[selected_item] == 'Volume Up':
                                self.change_volume(0.1)  # Увеличиваем громкость на 0.1
                            elif self.settings_items[selected_item] == 'Volume Down':
                                self.change_volume(-0.1)  # Уменьшаем громкость на 0.1
                            else:
                                print(f"Вы выбрали {self.settings_items[selected_item]}")

            items = self.menu_items if self.state == 'main' else self.settings_items

            for index, item in enumerate(items):
                color = (255, 255, 255)

                # Получение координат курсора
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Проверка, находится ли курсор над текущей кнопкой
                if (self.WIDTH // 2 - pixel_font.size(item)[0] // 2) < mouse_x < (self.WIDTH // 2 + pixel_font.size(item)[0] // 2) and \
                        (self.HEIGHT // 2 - pixel_font.size(item)[1] // 2 + index * vertical_spacing) < mouse_y < \
                        (self.HEIGHT // 2 - pixel_font.size(item)[1] // 2 + (index + 1) * vertical_spacing):
                    color = (255, 0, 0)  # Красный цвет при наведении
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.state == 'main':
                            if item == 'Exit':
                                pygame.quit()
                                sys.exit()
                            elif item == 'Settings':
                                self.state = 'settings'
                            else:
                                print(f"Вы выбрали {item}")
                        elif self.state == 'settings':
                            if item == 'Back':
                                self.state = 'main'
                            elif item == 'Volume Up':
                                self.change_volume(0.1)  # Увеличиваем громкость на 0.1
                            elif item == 'Volume Down':
                                self.change_volume(-0.1)  # Уменьшаем громкость на 0.1
                            else:
                                print(f"Вы выбрали {item}")

                label = pixel_font.render(item, True, color)
                screen.blit(label,
                            (self.WIDTH // 2 - label.get_width() // 2, self.HEIGHT // 2 - label.get_height() // 2 + index * vertical_spacing))

            # Обновление дисплея
            pygame.display.flip()


if __name__ == "__main__":
    menu = Menu()
    menu.main()
