from random import randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 30

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """
    Базовый класс создания объекта, от
    которого наследуются другие объекты
    """

    def __init__(self, position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
                 body_color=None):
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color

    def draw(self):
        """Определяет как объект отрисовывается на экране"""
        pass


class Snake(GameObject):
    """Класс Змейка - дочерний класс GameObject"""

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color)
        self.body_color = body_color
        self.direction = RIGHT
        self.next_direction = None
        self.positions = [self.position]
        self.length = 1
        self.last = None

    def draw(self, surface):
        """Метод рисует объект на игровом поле"""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def move(self):
        """Метод, отвечающий за перемещения объекта по игровому полю"""
        head_x, head_y = self.positions[0]
        delta_x, delta_y = self.direction

        position = (
            (head_x + (delta_x * GRID_SIZE)) % SCREEN_WIDTH,
            (head_y + (delta_y * GRID_SIZE)) % SCREEN_HEIGHT
        )
        self.positions.insert(0, position)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Получение координат головы змейки"""
        return self.positions[0]

    def reset(self):
        """Возвращение змейки в исходное состояние"""
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.positions = [self.position]
        self.direction = RIGHT
        self.length = 1


class Apple(GameObject):
    """Класс Яблоко - дочерний класс GameObject"""

    def __init__(self, body_color=APPLE_COLOR):
        super().__init__(body_color)
        self.body_color = body_color
        self.position = self.randomize_position()

    def randomize_position(self):
        """Вычисление случайной позиции яблока"""
        return (
            randint(1, GRID_WIDTH) * GRID_SIZE,
            randint(1, GRID_HEIGHT) * GRID_SIZE
        )

    def draw(self, surface):
        """Метод отрисовывает объект на игровом поле"""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


def handle_keys(game_object):
    """Функция, которая обрабатывает действия пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Функция представляющая логику игры"""
    apple = Apple()
    snake = Snake()
    screen.fill(BOARD_BACKGROUND_COLOR)

    def eat_apple():
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position()

    while True:

        clock.tick(SPEED)

        handle_keys(snake)

        eat_apple()

        snake.update_direction()

        snake.move()

        snake.draw(screen)

        apple.draw(screen)

        pygame.display.update()

        if snake.get_head_position() in snake.positions[2:]:
            snake.reset()


if __name__ == '__main__':

    main()
