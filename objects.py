import os
import keyboard
from time import sleep
from functools import partial
from random import choice, randint


class Cell:
    default = '.'
    apple = 'A'
    snake = '0'

    def __init__(self, content: str = default):
        # содержимое ячейки
        self.content = content

    def __bool__(self) -> bool:
        """
        False, если в ячейки пуста(имеет значение #)
        True в противном случае.
        """
        return self.content != self.default


class Snake:
    def __init__(self, points: list[list]):
        # координаты точек змейки
        self.points = points

    def __iter__(self):
        yield from self.points

    def grow(self, x: int, y: int) -> None:
        """
        Отвечает за рост змейки.
        Добавляет в список points новый кортеж с
        координатами точки.
        """
        self.points.insert(0, [x, y])

    def del_last_point(self) -> list:
        """
        Удаляет последнюю точку в списке координат
        тела змеи. Это нужно для создания эффекта
        движения змейки по полю.
        """
        return self.points.pop(-1)


class Field:
    def __init__(self, snake: Snake, x_len: int = 16, y_len: int = 16):
        # длина по вертикали
        self.x_len = x_len

        # длина по горизонтали
        self.y_len = y_len

        # игровое поле
        self.field = [[Cell() for _ in range(y_len)] for _ in range(x_len)]

        # генерим кол-во яблочек
        self.apples = randint(round(x_len / 2), x_len)
        # множество координат яблочек
        self.apples_points = set()
        # генерим коорды яблочек
        while len(self.apples_points) != self.apples:
            x, y = randint(0, self.x_len - 1), randint(0, self.y_len - 1)
            self.apples_points.add((x, y))
        # вставляем яблочки
        for x, y in self.apples_points:
            print(x, y, len(self.field))
            self.field[x][y] = Cell(content=Cell.apple)

        # объект змейки
        self.snake = snake

        # координата головы
        self.x_head, self.y_head = self.snake.points[0]

        # True, если игрок победил. False, если игрок проиграл или игра продолжается
        self.is_win = False
        # True, если игрок проиграл, False если победил или игра продолжается
        self.is_gameover = False

    def game_status(self) -> str:
        if self.is_win:
            return 'win'
        elif self.is_gameover:
            return 'gameover'
        else:
            return 'game'

    def show(self, width: str = 1 * ' ', height: str = '\n') -> None:
        """
        Выводит на экран содержимое поля
        width - символ между столбцами
        height - символ между строками
        """
        for row in self.field:
            print('\t' * 5, end='')
            for cell in row:
                print(cell.content, end=width)
            print(height, end='')

    def move_snake(self, direction: str):
        """
        Пересчитывает координаты в зависимости
        от нажатой клавиши.
        direction - это направление движения змейки.
        """
        # инкремент/декремент в зависимости от нажатой кнопки
        if direction == 'UP':
            self.y_head -= 1
        elif direction == 'DOWN':
            self.y_head += 1
        elif direction == 'LEFT':
            self.x_head -= 1
        elif direction == 'RIGHT':
            self.x_head += 1

        # если змейка вышла за пределы строк
        if self.y_head < 0:
            self.y_head = self.y_len - 1
        elif self.y_head > self.y_len - 1:
            self.y_head = 0

        # если змейка вышла за пределы столбцов
        if self.x_head < 0:
            self.x_head = self.x_len - 1
        elif self.x_head > self.x_len - 1:
            self.x_head = 0

        # добавляем в новую часть змейки
        self.snake.grow(self.x_head, self.y_head)

        # если змейка скушала яблоко, то удалять хвост не нужно
        if self.field[self.y_head][self.x_head].content != Cell.apple:
            x_del, y_del = self.snake.del_last_point()
            # устанавливает значок поля вместо точки змейки
            self.field[y_del][x_del].content = Cell.default
        else:
            self.apples -= 1
            # условие победы
            if self.apples == 0:
                self.is_win = True

        # вставляем по координатам символ змейки в field
        for x, y in self.snake:
            self.field[y][x].content = Cell.snake


class GameManager:
    """
    Класс отвечающий за управление
    """
    def __init__(self):
        # создаём объект игрового поля
        self.s = Snake(
            [
                [1, 1],
                [1, 2],
            ]
        )
        self.f = Field(snake=self.s)

        # кнопки и направления
        self.keys_directs = {
            ('w', 'up'): 'UP',
            ('s', 'down'): 'DOWN',
            ('a', 'left'): 'LEFT',
            ('d', 'right'): 'RIGHT',
        }

        # рандомно дёргаем начальное направление змейки
        self.direction = choice(tuple(self.keys_directs.values()))

        # регаем кнопки управления
        for keys, direction in self.keys_directs.items():
            event = partial(self.__set_direction, direction)
            for key in keys:
                keyboard.add_hotkey(key, event)

        # задержка перехода между ячейками
        self.delay = 0.2

    def __set_direction(self, direction: str):
        """
        Меняет направление движения змейки.
        Возможно будет перенесён в класс Snake"""
        self.direction = direction

    def play(self) -> None:
        """Запускает игровой цикл"""
        while self.f.game_status() == 'game':
            os.system('cls')
            print(self.direction)
            self.f.move_snake(self.direction)
            self.f.show()
            sleep(self.delay)

        if self.f.game_status() == 'win':
            print('\t\t\t\tТы победил!')
        elif self.f.game_status() == 'gameover':
            print('\t\t\t\tТы проиграл!')


if __name__ == '__main__':
    manager = GameManager()
    manager.play()