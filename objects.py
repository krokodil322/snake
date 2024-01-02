import os
import keyboard
import pickle
from time import sleep
from functools import partial
from random import choice, randint
from collections import deque
from copy import deepcopy
from datetime import datetime
from typing import Optional


class Cell:
    default = '.'
    apple = 'A'
    snake = '0'
    let = '#'

    def __init__(self, content: str = default):
        # содержимое ячейки
        self.content = content


class Snake:
    def __init__(self, start_points: list[tuple]):
        # координаты точек змейки
        self.points = deque(start_points)

    def __iter__(self):
        yield from self.points

    def __len__(self) -> int:
        return len(self.points)

    def grow(self, row: int, col: int) -> None:
        """
        Отвечает за рост змейки.
        Добавляет в список points новый кортеж с
        координатами точки.
        """
        self.points.appendleft((row, col))

    def del_last_point(self) -> tuple:
        """
        Удаляет последнюю точку в списке координат
        тела змеи. Это нужно для создания эффекта
        движения змейки по полю.
        """
        return self.points.pop()


class Field:
    """
    Класс описывающий игровое поле.

    Стандартное поле 16x16 и его ориентация:

                    y_len
    0 ----------------------------------> y, col
    |   . . . . . . . . . . . . . . . .
    |   . . . . . . . . . . . . . . . .
    |   . . . . . . . . . . . . . . . .
    |   . . . . . . . . . . . . . . . .
    |   . . . . . . . . . . . . . . . .
    |   . . . . . . . . . . . . . . . .
    |   . . . . . . . . . . . . . . . .
    |   . . . . . . . . . . . . . . . .
    |   . . . . . . . . . . . . . . . .
    |   . . . . . . . . . . . . . . . .
    |   . . . . . . . . . . . . . . . .
    |   . . . . . . . . . . . . . . . .
    |   . . . . . . . . . . . . . . . .
    |   . . . . . . . . . . . . . . . .
    |   . . . . . . . . . . . . . . . .
    |   . . . . . . . . . . . . . . . .
    V
    x, row
    """

    def __init__(
        self,
        snake: Snake,
        x_len: int = 16,
        y_len: int = 16,
    ):
        # длина по вертикали
        self.x_len = x_len

        # длина по горизонтали
        self.y_len = y_len

        # игровое поле
        self.field = [[Cell() for _ in range(y_len)] for _ in range(x_len)]

        # объект змейки
        self.snake = snake

        # генерим кол-во яблочек
        middle = round((x_len + y_len) / 2)
        self.apples = randint(round(middle / 2), middle)

        # сохраняем коорды яблочек в список(для перепросмотра сессии)
        self.apples_points = deque([])

        # вставляем яблочки старая механика
        # теперь яблочки вставляются по очереди
        # for x, y in self.apples_points:
        #     self.field[x][y] = Cell(content=Cell.apple)

        # вставляем первое яблочко
        row, col = self.__generate_apple_point()
        self.field[row][col].content = Cell.apple

        # координата головы
        self.row_head, self.col_head = self.snake.points[0]

        # True, если игрок победил. False, если игрок проиграл или игра продолжается
        self.is_win = False
        # True, если игрок проиграл, False если победил или игра продолжается
        self.is_gameover = False

    def __generate_apple_point(self) -> tuple:
        while True:
            row, col = randint(0, self.x_len - 1), randint(0, self.y_len - 1)
            if (row, col) not in self.snake \
               and self.field[row][col].content != Cell.let:
                return row, col

    def game_status(self) -> str:
        if self.is_win:
            return 'win'
        elif self.is_gameover:
            return 'gameover'
        else:
            return 'game'

    def __str__(self) -> str:
        string = ''
        for row in self.field:
            string += ''.join(map(
                lambda cell: cell.content, row)) + '\n'
        return string

    def show(
            self,
            width: str = 1 * ' ',
            height: str = '\n'
    ) -> None:
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

    def set_field_by_sample(
            self,
            sample: str,
            apples: int
    ) -> None:
        """
        Создаёт новое поле field
        на основании шаблона sample
        """
        sample = list(map(list, sample.split('\n')))
        self.field = []
        self.apples = apples
        for r_index, row in enumerate(filter(None, sample)):
            self.field.append([])
            for c_index, cell in enumerate(
                    filter(lambda char: char != ' ', row)
            ):
                if cell == Cell.apple:
                    # исключаем случай когда пытаемся
                    # вставить змейку в ячейку с яблоком
                    for row_snake, col_snake in self.snake:
                        if (r_index, c_index) == (row_snake, col_snake):
                            raise ValueError(
                                f'Змейка не может заспавниться в точке {(row_snake, col_snake)}\n'
                                f'Ибо в этой точке спавнится яблоко'
                            )
                    self.field[r_index].append(
                        Cell(content=Cell.default)
                    )
                else:
                    self.field[r_index].append(
                        Cell(content=cell)
                    )
        self.__insert_apple()
        self.apples_points.clear()

    def move_snake(
            self,
            direction: str,
            gen_apple: bool = True,
    ) -> None:
        """
        Пересчитывает координаты в зависимости
        от нажатой клавиши.
        direction - это направление движения змейки.
        """
        # инкремент/декремент в зависимости от нажатой кнопки
        if direction == 'UP':
            self.row_head -= 1
        elif direction == 'DOWN':
            self.row_head += 1
        elif direction == 'LEFT':
            self.col_head -= 1
        elif direction == 'RIGHT':
            self.col_head += 1

        # если змейка вышла за пределы строк
        if self.row_head < 0:
            self.row_head = self.x_len - 1
        elif self.row_head > self.x_len - 1:
            self.row_head = 0

        # если змейка вышла за пределы столбцов
        if self.col_head < 0:
            self.col_head = self.y_len - 1
        elif self.col_head > self.y_len - 1:
            self.col_head = 0

        # добавляем новую часть змейки
        # для имитации её движения
        self.snake.grow(self.row_head, self.col_head)

        head_content = self.field[self.row_head][self.col_head].content

        # если змейка скушала яблоко, то удалять хвост не нужно
        if head_content == Cell.default:
            row_del, col_del = self.snake.del_last_point()
            # устанавливает значок поля вместо точки змейки
            self.field[row_del][col_del].content = Cell.default
        elif head_content == Cell.apple:
            self.apples -= 1
            # условие победы
            # на всякий поставил <=
            if self.apples <= 0:
                self.is_win = True
            # вставляем следующее яблочко
            if gen_apple:
                self.__insert_apple()
            else:
                try:
                    row, col = self.apples_points.popleft()
                    self.field[row][col].content = Cell.apple
                except IndexError:
                    pass
        elif head_content in (Cell.let, Cell.snake):
            # условие поражения
            self.is_gameover = True
            return None

        # вставляем по координатам символ змейки в field
        for row, col in self.snake:
            self.field[row][col].content = Cell.snake

    def __insert_apple(self) -> None:
        """Вставляет одно яблоко в поле field"""
        if self.apples > 0:
            row, col = self.__generate_apple_point()
            self.apples_points.append((row, col))
            self.field[row][col].content = Cell.apple


class GameManager:
    """
    Класс отвечающий за взаимодействие с игроком
    """
    # всего есть 5 уровней
    ALL_LEVELS = (1, 2, 3, 4, 5)

    def __init__(
            self,
            snake: Snake,
            field: Field,
            delay: float = 0.2,
            direction: Optional[str] = None,
    ):
        # на всяки пожарный создадим объект змейки
        self.snake = snake

        # создаём объект игрового поля
        self.field = field

        # кнопки и направления
        self.keys_directs = {
            ('w', 'up'): 'UP',
            ('s', 'down'): 'DOWN',
            ('a', 'left'): 'LEFT',
            ('d', 'right'): 'RIGHT',
        }

        if not direction:
            # рандомно дёргаем начальное направление змейки
            self.direction = choice(tuple(self.keys_directs.values()))
        else:
            self.direction = direction

        # регаем кнопки
        self.set_keys()

        # задержка перехода между ячейками
        self.delay = delay

        # для сохранения сессии
        self.session = {
            'field': deepcopy(self.field),
            'delay': deepcopy(self.delay),
            'iter_key': [],
            'apples_points': deque([]),
        }

        # название папки с логами
        self.logs_dir = 'logs'

    def set_keys(self) -> None:
        """Регает кнопки управления"""
        for keys, direction in self.keys_directs.items():
            event = partial(self.__set_direction, direction)
            for key in keys:
                keyboard.add_hotkey(key, event)

    def __set_direction(self, direction: str) -> None:
        """
        Меняет направление движения змейки.
        Возможно будет перенесён в класс Snake
        """

        horizontal = ('UP', 'DOWN')
        vertical = ('LEFT', 'RIGHT')

        if self.direction in horizontal and direction in vertical \
           or self.direction in vertical and direction in horizontal:
            self.direction = direction

    def play(self, save_logs: bool = True) -> None:
        """
        Запускает игровой цикл
        save_logs: bool - сохранять ли логи сессии
        """
        self.set_keys()
        iter_key = 0
        while self.field.game_status() == 'game':
            os.system('cls')
            self.session['iter_key'].append(
                (iter_key, deepcopy(self.direction))
            )
            self.field.move_snake(self.direction)
            self.field.show()
            sleep(self.delay)
            iter_key += 1

        if self.field.game_status() == 'win':
            print('Ты победил!')
        elif self.field.game_status() == 'gameover':
            print('Ты проиграл!')

        self.session['apples_points'] = deepcopy(
            self.field.apples_points
        )

        if save_logs:
            # сохраняем логи сессии
            self.logs()

    def logs(self, filename: Optional[str] = None) -> None:
        """
        Записывается весь путь пройденный
        змейкой в виде кол-ва итераций и
        нажатых игороком кнопок за весь матч

        filename - имя файла с кэшэм сессии.
        Создаётся автоматически по дате и времени
        окончания сессии, но можно указать своё
        значение.
        """
        try:
            os.mkdir(self.logs_dir)
        except FileExistsError:
            pass

        if not filename:
            filename = datetime.now().strftime('%d.%m.%Y %H-%M-%S')

        with open(f'{self.logs_dir}/{filename}.pkl', 'wb') as file:
            pickle.dump(self.session, file)

    @staticmethod
    def get_user_index(dir: list) -> str:
        """
        Принимает данные от юзера
        Возвращает введённую строку, если она число.
        """
        while True:
            index = None
            try:
                index = int(input('Введи номер: '))
            except TypeError:
                print(f'\tИндекс должен быть числом(int)!')

            while index:
                try:
                    return dir[index - 1]
                except IndexError:
                    print('Файла с таким номером не существует!')
                    break

    def show_repeat(self) -> None:
        """
        Показывает на экране уже отыгранную сессию.
        Информацию о сессии берёт из папки logs
        """
        files = os.listdir(self.logs_dir)
        if len(files) == 0:
            print('Игровых сессий не найдено.')
            return None

        for index, filename in enumerate(files, 1):
            print(f'{index}. {filename}')

        filename = self.get_user_index(dir=files)

        with open(f'{self.logs_dir}/{filename}', 'rb') as file:
            session = pickle.load(file)

        if session:
            self.field = session['field']
            self.field.apples_points = session['apples_points']
            self.delay = session['delay']

            for _, direction in session['iter_key']:
                os.system('cls')
                self.__set_direction(direction)
                # устанавливаем режим когда яблоки генерить не нужно
                # тогда move_snake будет их пытаться дёргать из
                # списка self.apples_points
                self.field.move_snake(
                    self.direction,
                    gen_apple=False,
                )
                self.field.show()
                sleep(self.delay)

    @staticmethod
    def get_game_by_lvl(lvl: int) -> 'GameManager':
        """
        Возвращает объект(лвл) класса GameManager из папки lvls
        по указанному уровню
        """
        with open(f'lvls/{str(lvl)}.pkl', 'rb') as file:
            return pickle.load(file)

    @classmethod
    def create_lvl(
            cls,
            lvl: int,
            snake: Snake,
            field: Field,
            delay: float = 0.2,
            direction: Optional[str] = None,
    ) -> None:
        """
        Метод для создания нового лвла. По заданным
        харам создаёт объект класса GameManager и
        добавляет его в папку lvls в формате .pkl
        """
        if lvl not in cls.ALL_LEVELS:
            raise ValueError(
                f'Все возможные номера лвлов: {cls.ALL_LEVELS}'
                f'Твой лвл не входит в этот список: {lvl}'
            )

        try:
            os.mkdir('lvls')
        except FileExistsError:
            pass

        with open(f'lvls/{str(lvl)}.pkl', 'wb') as file:
            obj_lvl = cls(
                snake=snake,
                field=field,
                delay=delay,
                direction=direction,
            )
            pickle.dump(obj_lvl, file)


if __name__ == '__main__':
    # snake = Snake(start_points=[(1, 1), (1, 2)])
    # field = Field(snake=snake)
    # manager = GameManager(snake=snake, field=field)
    # manager.play()

    # GameManager.create_lvl(1)
    pass
