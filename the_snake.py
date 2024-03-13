from random import randint

import pygame

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

KEYBOARD_MOVES = {
    (pygame.K_UP, LEFT): UP,
    (pygame.K_UP, RIGHT): UP,
    (pygame.K_DOWN, LEFT): DOWN,
    (pygame.K_DOWN, RIGHT): DOWN,
    (pygame.K_LEFT, UP): LEFT,
    (pygame.K_LEFT, DOWN): LEFT,
    (pygame.K_RIGHT, UP): RIGHT,
    (pygame.K_RIGHT, DOWN): RIGHT,
}

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
SPEED = 30

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption(f'Змейка. Клавиши управления:'
                           f'(← - налево; → - направо;'
                           f'↑ - вверх; ↓ - вниз). Скорость = {SPEED}')
clock = pygame.time.Clock()


class GameObject:
    """
    Базовый класс создания объекта, от
    которого наследуются другие объекты
    """

    def __init__(self, position=None,
                 body_color=None):
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color

    def draw(self):
        """Определяет как объект отрисовывается на экране"""
        raise NotImplementedError

    def draw_elements(self, position, color):
        """Метод отрисовывающий элементы объектов"""
        pygame.draw.rect(screen, self.body_color,
                         (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
                         )
        pygame.draw.rect(screen, color,
                         (pygame.Rect(position, (GRID_SIZE, GRID_SIZE))), 1)


class Snake(GameObject):
    """Класс Змейка - дочерний класс GameObject"""

    def __init__(self):
        super().__init__(body_color=SNAKE_COLOR)
        self.direction = RIGHT
        self.next_direction = None
        self.positions = [self.position]
        self.length = 1
        self.last = None

    def draw(self):
        """Метод рисует объект на игровом поле"""
        for position in self.positions[:-1]:
            GameObject.draw_elements(self, (position[0], position[1]),
                                     color=BORDER_COLOR)

        GameObject.draw_elements(self, self.positions[0], color=BORDER_COLOR)

        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

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

    def draw(self):
        """Метод отрисовывает объект на игровом поле"""
        GameObject.draw_elements(self, (self.position[0], self.position[1]),
                                 color=BORDER_COLOR)


def handle_keys(game_object):
    """Функция, которая обрабатывает действия пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        elif event.type == pygame.KEYDOWN:
            for move in KEYBOARD_MOVES:
                if event.key == move[0] and game_object.direction != move[1]:
                    game_object.next_direction = KEYBOARD_MOVES[move]


def main():
    """Функция представляющая логику игры"""
    apple = Apple()
    snake = Snake()

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
        snake.draw()
        apple.draw()
        pygame.display.update()

        if snake.get_head_position() in snake.positions[2:]:
            snake.reset()


if __name__ == '__main__':

    main()
