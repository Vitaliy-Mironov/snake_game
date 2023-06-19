import pygame
import random
import os
from pygame.locals import *

# Инициализация Pygame
pygame.init()

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Размеры окна и сегментов змеи
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
SEGMENT_SIZE = 20

# Создание окна игры
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()

# Инициализация звуковых эффектов
pygame.mixer.init()
current_directory = os.path.dirname(os.path.abspath(__file__))
eat_sound = pygame.mixer.Sound(
    os.path.join(current_directory, "sounds", "eat.wav"))
game_over_sound = pygame.mixer.Sound(
    os.path.join(current_directory, "sounds", "game_over.wav"))


# Функция для отрисовки змейки
def draw_snake(snake_segments):
    for segment in snake_segments:
        pygame.draw.circle(
            window, GREEN,
            (segment[0] + SEGMENT_SIZE // 2, segment[1] + SEGMENT_SIZE // 2),
            SEGMENT_SIZE // 2)


# Функция для отрисовки еды
def draw_food(food_position):
    pygame.draw.circle(window, RED, (food_position[0] + SEGMENT_SIZE // 2,
                                     food_position[1] + SEGMENT_SIZE // 2),
                       SEGMENT_SIZE // 2)


# Функция для отображения текста на экране
def display_text(text, x, y, font_size=24, color=WHITE):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    window.blit(text_surface, text_rect)


# Функция для запуска новой игры
def new_game():
    game()


# Функция для отображения сообщения о завершении игры
def game_over(score):
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            elif event.type == KEYDOWN:
                if event.key == K_x:
                    pygame.quit()
                    return
                elif event.key == K_g:
                    new_game()

        window.fill(BLACK)
        display_text(f"Игра окончена. Ваш счет: {score}", WINDOW_WIDTH // 2,
                     WINDOW_HEIGHT // 2 - 20)
        display_text("Закрыть игру - X", WINDOW_WIDTH // 2,
                     WINDOW_HEIGHT // 2 + 20)
        display_text("Новая игра - G", WINDOW_WIDTH // 2,
                     WINDOW_HEIGHT // 2 + 60)
        pygame.display.flip()


# Главная функция игры
def game():
    # Переменные для змейки
    snake_segments = [[WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2]]
    direction = 'right'
    growing = False

    # Переменные для еды
    food_position = [
        random.randint(0, (WINDOW_WIDTH - SEGMENT_SIZE) // SEGMENT_SIZE) *
        SEGMENT_SIZE,
        random.randint(0, (WINDOW_HEIGHT - SEGMENT_SIZE) // SEGMENT_SIZE) *
        SEGMENT_SIZE
    ]

    # Переменные для счета
    score = 0

    # Флаги состояния игры
    game_started = False
    game_paused = False

    # Основной игровой цикл
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_g:
                    game_started = True
                elif event.key == K_p:
                    game_paused = not game_paused
                elif event.key == K_x:
                    running = False
                elif game_started and not game_paused:
                    if event.key == K_UP and direction != 'down':
                        direction = 'up'
                    elif event.key == K_DOWN and direction != 'up':
                        direction = 'down'
                    elif event.key == K_LEFT and direction != 'right':
                        direction = 'left'
                    elif event.key == K_RIGHT and direction != 'left':
                        direction = 'right'

        if not game_started:
            window.fill(BLACK)
            display_text("Начать игру - G, пауза - P, закрыть игру - X",
                         WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
            display_text(
                "Управление змейкой: Стрелки (Вверх, Вниз, Влево, Вправо)",
                WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40)
            pygame.display.flip()
            continue

        if game_paused:
            window.fill(BLACK)
            display_text("Пауза - P", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
            pygame.display.flip()
            continue

        # Обработка движения змейки
        if direction == 'up':
            new_segment = [
                snake_segments[0][0], snake_segments[0][1] - SEGMENT_SIZE
            ]
        elif direction == 'down':
            new_segment = [
                snake_segments[0][0], snake_segments[0][1] + SEGMENT_SIZE
            ]
        elif direction == 'left':
            new_segment = [
                snake_segments[0][0] - SEGMENT_SIZE, snake_segments[0][1]
            ]
        elif direction == 'right':
            new_segment = [
                snake_segments[0][0] + SEGMENT_SIZE, snake_segments[0][1]
            ]

        snake_segments.insert(0, new_segment)

        # Проверка столкновения с границами окна
        if (snake_segments[0][0] < 0 or snake_segments[0][0] >= WINDOW_WIDTH
                or snake_segments[0][1] < 0
                or snake_segments[0][1] >= WINDOW_HEIGHT):
            break

        # Проверка столкновения с самой змейкой
        if snake_segments[0] in snake_segments[1:]:
            break

        # Проверка столкновения с едой
        if snake_segments[0] == food_position:
            growing = True
            food_position = [
                random.randint(0,
                               (WINDOW_WIDTH - SEGMENT_SIZE) // SEGMENT_SIZE) *
                SEGMENT_SIZE,
                random.randint(0,
                               (WINDOW_HEIGHT - SEGMENT_SIZE) // SEGMENT_SIZE)
                * SEGMENT_SIZE
            ]
            score += 1
            eat_sound.play()

        # Удаление последнего сегмента змейки, если она не растет
        if not growing:
            snake_segments.pop()

        # Увеличение длины змейки
        growing = False

        # Отрисовка игрового поля
        window.fill(BLACK)
        draw_snake(snake_segments)
        draw_food(food_position)
        display_text(f"Счет: {score}", WINDOW_WIDTH // 2, 20)
        pygame.display.flip()

        # Ограничение скорости игры
        clock.tick(10)

    # Завершение игры
    game_over_sound.play()
    game_over(score)
    pygame.quit()


# Запуск игры
new_game()
