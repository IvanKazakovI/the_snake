import pygame
import pytest

import the_snake


EXPECTED_GAME_OBJECT_ATTRS = (
    ('атрибут', 'position'),
    ('атрибут', 'color'),
    ('метод', 'draw'),
)


@pytest.mark.parametrize(
    'attr_type, attr_name',
    EXPECTED_GAME_OBJECT_ATTRS,
    ids=[elem[1] for elem in EXPECTED_GAME_OBJECT_ATTRS]
)
def test_game_object_attributes(game_object, attr_type, attr_name):
    assert hasattr(game_object, attr_name), (
        f'Убедитесь, что у объектов класса `GameObject` определен {attr_type} '
        f'`{attr_name}`.'
    )


EXPECTED_APPLE_ATTRS = (
    ('атрибут', 'position'),
    ('атрибут', 'color'),
    ('метод', 'draw'),
    ('метод', '_randomize_position'),
)


def test_apple_inherits_from_game_object():
    assert issubclass(the_snake.Apple, the_snake.GameObject), (
        'Класс `Apple` должен наследоваться от класса `GameObject`.'
    )


@pytest.mark.parametrize(
    'attr_type, attr_name',
    EXPECTED_APPLE_ATTRS,
    ids=[elem[1] for elem in EXPECTED_APPLE_ATTRS]
)
def test_apple_attributes(apple, attr_type, attr_name):
    assert hasattr(apple, attr_name), (
        f'Убедитесь, что у объектов класса `Apple` определен {attr_type} '
        f'`{attr_name}`.'
    )


EXPECTED_SNAKE_ATTRS = (
    ('атрибут', 'position'),
    ('атрибут', 'color'),
    ('атрибут', 'length'),
    ('атрибут', 'positions'),
    ('атрибут', 'direction'),
    ('атрибут', 'next_direction'),
    ('метод', 'draw'),
    ('метод', 'get_head_position'),
    ('метод', 'move'),
    ('метод', '_reset'),
    ('метод', 'handle_keys'),
    ('метод', 'update_direction'),
)


def test_snake_inherits_from_game_object():
    assert issubclass(the_snake.snake_, the_snake.GameObject), (
        'Класс `Snake` должен наследоваться от класса `GameObject`.'
    )


@pytest.mark.parametrize(
    'attr_type, attr_name',
    EXPECTED_SNAKE_ATTRS,
    ids=[elem[1] for elem in EXPECTED_SNAKE_ATTRS]
)
def test_snake_attributes(snake, attr_type, attr_name):
    assert hasattr(snake, attr_name), (
        f'Убедитесь, что у объектов класса `Snake` определен {attr_type} '
        f'`{attr_name}`.'
    )


EXPECTED_MODULE_ELEMENTS = (
    ('константа', 'SCREEN_WIDTH'),
    ('константа', 'SCREEN_HEIGHT'),
    ('константа', 'GRID_SIZE'),
    ('константа', 'GRID_WIDTH'),
    ('константа', 'GRID_HEIGHT'),
    ('константа', 'BACKGROUND_COLOR'),
    ('константа', 'UP'),
    ('константа', 'DOWN'),
    ('константа', 'LEFT'),
    ('константа', 'RIGHT'),
    ('переменная', 'screen'),
    ('переменная', 'clock'),
)


@pytest.mark.parametrize(
    'element_type, element_name',
    EXPECTED_MODULE_ELEMENTS,
    ids=[elem[1] for elem in EXPECTED_MODULE_ELEMENTS]
)
def test_elements_exist(element_type, element_name):
    assert hasattr(the_snake, element_name), (
        f'Убедитесь, что в модуле `the_snake` определена {element_type} '
        f'`{element_name}`.'
    )


@pytest.mark.parametrize(
    'expected_type, var_name',
    (
        (pygame.Surface, 'screen'),
        (pygame.time.Clock, 'clock'),
    ),
)
def test_vars_type(expected_type, var_name):
    assert isinstance(getattr(the_snake, var_name, None), expected_type), (
        'Убедитесь, что в модуле `the_snake` есть переменная '
        f'`{var_name}` типа `{expected_type.__name__}`.'
    )


def test_main_exists():
    assert hasattr(the_snake, 'main'), (
        'Убедитесь, что в модуле `the_snake` есть функция `main`.'
    )
