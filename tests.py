from objects import *

import unittest
from copy import deepcopy


class CellTest(unittest.TestCase):
    def setUp(self) -> None:
        self.cell = Cell()

    def test_attrs(self):
        self.assertTrue(
            all(
                hasattr(self.cell, attr)
                for attr in ('content', 'default')
            )
        )

    def test_default(self):
        self.assertTrue(self.cell.content == self.cell.default)


class SnakeTest(unittest.TestCase):
    def setUp(self):
        self.start_points = [(1, 1), (1, 2)]
        self.snake = Snake(
            points=deepcopy(self.start_points)
        )

    def test_iter(self):
        """Тест итерируемости объекта класса Snake"""
        for pack1, pack2 in zip(
                self.start_points,
                self.snake
        ):
            self.assertTrue(pack1 == pack2)

    def test_grow(self):
        """Тест метода grow класса Snake"""
        new_point = (1, 3)
        self.snake.grow(*new_point)
        self.assertTrue(new_point == self.snake.points[0])

    def test_del_last_point(self):
        """Тест метода del_last_point класса Snake"""
        del_point = self.snake.del_last_point()
        self.assertTrue(del_point == self.start_points[-1])


class FieldTest(unittest.TestCase):
    def setUp(self) -> None:
        self.start_points = [(1, 1), (1, 2)]
        self.snake = Snake(
            points=deepcopy(self.start_points)
        )
        self.field = Field(
            snake=self.snake
        )

    def test_field_attr(self):
        """
        Тест атрбута field класса Field
        Проверяем размерность игрового поля
        с заданными характеристиками
        """
        self.assertTrue(
            len(self.field.field) == self.field.x_len
        )
        for row in self.field.field:
            self.assertTrue(
                len(row) == self.field.y_len
            )

    def test_generate_apples(self):
        """
        Тест атрибуты field класса Field
        Проверяем генерацию ябочек в поле
        """
        apples = 0
        for row in self.field.field:
            for cell in row:
                if cell.content == Cell.apple:
                    apples += 1
        self.assertTrue(
            self.field.apples == apples
        )

    def test_game_status(self):
        """Тест метода game_status класса Field"""
        self.assertTrue(
            self.field.game_status(), 'game'
        )

        self.field.is_win = True
        self.assertTrue(
            self.field.game_status(), 'win'
        )
        self.field.is_win = True

        self.field.is_gameover = True
        self.assertTrue(
            self.field.game_status(), 'gameover'
        )

    def test_show(self):
        """Тест метода show класса Field"""
        pass

    def test_move_snake(self):
        """
        Тест главного метода класса Field
        Тест движений по вертикали
        """
        y_head = self.field.y_head

        # тест движения вверх
        # простой случай
        self.field.move_snake('UP')
        self.assertTrue(
            self.field.y_head == y_head - 1
        )
        # когда выходит за пределы строк при декременте
        self.field.move_snake('UP')
        # должен быть равен кол-ву строк в матрице - 1
        self.assertTrue(
            self.field.y_head == self.field.y_len - 1
        )

        self.field.move_snake('UP')
        self.field.move_snake('UP')
        y_head = self.field.y_head
        # тест движения вниз
        # простой случай
        self.field.move_snake('DOWN')
        self.assertTrue(
            self.field.y_head == y_head + 1
        )
        # когда выходит за пределы строк при инкременте
        self.field.move_snake('DOWN')
        self.field.move_snake('DOWN')

        self.assertTrue(
            self.field.y_head == 0
        )

    def test_move_snake_2(self):
        """
        Тест главного метода класса Field
        Тест движений по горизонтали
        """
        x_head = self.field.x_head

        # движение влево
        # простой случай
        self.field.move_snake('LEFT')
        self.assertTrue(
            self.field.x_head == x_head - 1
        )
        # когда выходит за границы столбцов при декременте
        self.field.move_snake('LEFT')
        self.assertTrue(
            self.field.x_head == self.field.x_len - 1
        )
        self.field.move_snake('LEFT')
        self.field.move_snake('LEFT')

        x_head = self.field.x_head
        # движение вправо
        # простой случай
        self.field.move_snake('RIGHT')
        self.assertTrue(
            self.field.x_head == x_head + 1
        )
        # когда выходит за границы столбцов при инкременте
        self.field.move_snake('RIGHT')
        self.field.move_snake('RIGHT')
        self.assertTrue(
            self.field.x_head == 0
        )

    def test_move_snake_3(self):
        """
        Тест главного метода класса Field
        Тест на размер змейки при прохождении
        обычной ячейки
        """
        self.field.field[1][0].content = Cell.default
        size_before = len(self.field.snake)
        self.field.move_snake('LEFT')
        self.assertTrue(
            len(self.field.snake) == size_before
        )

    def test_move_snake_4(self):
        """
        Тест главного метода класса Field
        Тест на съедание яблочка змейкой
        """
        if self.field.field[1][0].content != Cell.apple:
            self.field.field[1][0].content = Cell.apple
            self.field.apples += 1
        apples = self.field.apples
        size_before = len(self.field.snake)
        self.field.move_snake('LEFT')
        self.assertTrue(
            len(self.field.snake) == size_before + 1
        )
        self.assertTrue(
            self.field.apples == apples - 1
        )

    def test_move_snake_5(self):
        """
        Тест главного метода класса Field
        Тест на съедание яблочка змейкой
        с условием победы
        """
        # перегенерим нужным образом яблоки
        for row in self.field.field:
            for cell in row:
                cell.content = Cell.default

        self.field.apples = 0
        self.field.apples_points.clear()

        self.field.field[1][0].content = Cell.apple
        self.field.apples += 1

        self.assertFalse(self.field.is_win)
        self.field.move_snake('LEFT')
        self.assertTrue(self.field.is_win)
        self.assertTrue(
            self.field.apples == 0
        )

    def test_move_snake_6(self):
        """
        Тест главного метода класса Field
        Тест на добавление в ячейку Cell
        поля Field символа змейки '0'
        при применении метода move_snake
        """
        self.field.move_snake('RIGHT')
        for row, col in self.field.snake:
            self.assertTrue(
                self.field.field[col][row].content == \
                '0'
            )







if __name__ == '__main__':
    unittest.main()
