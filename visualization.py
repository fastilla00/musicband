import pygame
import sys

# Инициализация визуализации
def initialize_visualization():
    pygame.init()
    global screen, clock

    # Настройка окна
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Music Visualization")
    clock = pygame.time.Clock()

# Обновление визуализации на основе параметров
def update_visualization(params):
    pitch = params.get("pitch", 60)  # Нота
    volume = params.get("volume", 0.5)  # Громкость (0-1)
    tempo = params.get("tempo", 120)  # Темп

    # Цвет зависит от высоты звука (pitch)
    color = (pitch % 128 * 2, 255 - (pitch % 128 * 2), (pitch * 3) % 255)

    # Размер зависит от громкости (volume)
    size = int(volume * 200)

    # Очистка экрана
    screen.fill((0, 0, 0))

    # Отрисовка шара в центре
    pygame.draw.circle(screen, color, (400, 300), size)

    # Обновление экрана
    pygame.display.flip()

    # Регулировка частоты обновления
    clock.tick(tempo)

# Завершение визуализации
def stop_visualization():
    pygame.quit()

# Тестирование визуализации (опционально)
if __name__ == "__main__":
    initialize_visualization()
    try:
        while True:
            # Пример параметров для теста
            test_params = {
                "pitch": 60,
                "volume": 0.7,
                "tempo": 60
            }
            update_visualization(test_params)

            # Проверка событий выхода
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    except KeyboardInterrupt:
        stop_visualization()
