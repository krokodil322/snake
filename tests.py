from objects import *

import unittest


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
            start_points=deepcopy(self.start_points)
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
            start_points=deepcopy(self.start_points)
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

    def test_generate_apple_point(self):
        """Тест метода __generate_apple_point"""
        # перегенерим змейку специальным образом
        # сделаем так, чтобы она занимала половину всего поля
        start_points = []
        for row in range(round(self.field.x_len / 2)):
            for col in range(round(self.field.y_len / 2)):
                start_points.append((row, col))
        new_snake = Snake(start_points=start_points)
        new_field = Field(snake=new_snake)
        for _ in range(1000):
            x, y = new_field._Field__generate_apple_point()
            self.assertTrue(
                (y, x) not in new_snake
            )



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

    # def test_move_snake_5(self):
    #     """
    #     Тест главного метода класса Field
    #     Тест на съедание яблочка змейкой
    #     с условием победы
    #     """
    #     # перегенерим нужным образом яблоки
    #     for row in self.field.field:
    #         for cell in row:
    #             cell.content = Cell.default
    #
    #     self.field.apples = 0
    #     self.field.apples_points.clear()
    #
    #     self.field.field[1][0].content = Cell.apple
    #     self.field.apples += 1
    #
    #     self.assertFalse(self.field.is_win)
    #     self.field.move_snake('LEFT')
    #     self.assertTrue(self.field.is_win)
    #     self.assertTrue(
    #         self.field.apples == 0
    #     )

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
                self.field.field[col][row].content == '0'
            )

    def test_set_field_by_sample(self):
        lvl_2 = """
            .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
            .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
            .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
            .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
            .  .  .  .  #  .  .  .  .  .  .  #  .  .  .  .
            .  .  .  .  #  .  .  .  .  .  .  #  .  .  .  .
            .  .  .  .  #  .  .  .  .  .  .  #  .  .  .  .
            .  .  .  .  #  .  .  .  .  .  .  #  .  .  .  .
            .  .  .  .  #  .  .  .  .  .  .  #  .  .  .  .
            .  .  .  .  #  .  .  .  .  .  .  #  .  .  .  .
            .  .  .  .  #  .  .  .  .  .  .  #  .  .  .  .
            .  .  .  .  #  .  .  .  .  .  .  #  .  .  .  .
            .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
            .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
            .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
            .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
        """
        self.field.set_field_by_sample(
            sample=lvl_2,
            apples=10
        )

        sample = list(map(list, lvl_2.split('\n')))

        for old_row, new_row in zip(
            self.field.field, filter(None, sample)
        ):
            for old_cell, new_cell_content in zip(
                old_row,
                filter(lambda char: char != ' ', new_row)
            ):
                self.assertTrue(
                    old_cell.content == new_cell_content
                )

        sample = []
        for index, row in enumerate(
            map(list, lvl_2.split('\n'))
        ):
            sample.append([])
            for cell in filter(lambda char: char != ' ', row):
                sample[index].append(cell)

        sample[2][1] = Cell.apple
        sample = '\n'.join(map(''.join, sample))
        self.assertRaises(
            ValueError,
            self.field.set_field_by_sample,
            sample=sample,
            apples=10
        )


class TestGameManager(unittest.TestCase):
    def setUp(self) -> None:
        # размеры поля сессии
        self.x_len = self.y_len = 16

        # полные шаги сессии
        self.iter_key = [
            (0, 'UP'), (1, 'UP'), (2, 'UP'),
            (3, 'UP'), (4, 'UP'), (5, 'UP'),
            (6, 'LEFT'), (7, 'DOWN'), (8, 'DOWN'),
            (9, 'DOWN'), (10, 'DOWN'), (11, 'DOWN'),
            (12, 'DOWN'), (13, 'DOWN'), (14, 'RIGHT'),
            (15, 'RIGHT'), (16, 'RIGHT'), (17, 'DOWN'),
            (18, 'DOWN'), (19, 'DOWN'), (20, 'DOWN'),
            (21, 'DOWN'), (22, 'DOWN'), (23, 'DOWN'),
            (24, 'DOWN'), (25, 'DOWN'), (26, 'RIGHT'),
            (27, 'RIGHT'), (28, 'RIGHT'), (29, 'UP'),
            (30, 'UP'), (31, 'UP'), (32, 'UP'),
            (33, 'UP'), (34, 'LEFT'), (35, 'UP'),
            (36, 'UP'), (37, 'UP'), (38, 'UP'),
            (39, 'RIGHT'), (40, 'RIGHT'), (41, 'RIGHT'),
            (42, 'DOWN'), (43, 'DOWN'), (44, 'DOWN'),
            (45, 'DOWN'), (46, 'DOWN'), (47, 'DOWN'),
            (48, 'DOWN'), (49, 'DOWN'), (50, 'DOWN'),
            (51, 'DOWN'), (52, 'RIGHT'), (53, 'RIGHT'),
            (54, 'RIGHT'), (55, 'RIGHT'), (56, 'RIGHT'),
            (57, 'RIGHT'), (58, 'UP'), (59, 'UP'),
            (60, 'UP'), (61, 'UP'), (62, 'UP'),
            (63, 'UP'), (64, 'UP'), (65, 'UP'),
            (66, 'UP'), (67, 'UP'), (68, 'RIGHT'),
            (69, 'DOWN'), (70, 'DOWN'), (71, 'DOWN'),
            (72, 'DOWN'), (73, 'DOWN'), (74, 'DOWN'),
            (75, 'DOWN'), (76, 'DOWN'), (77, 'DOWN')
        ]
        # точки яблок сессии
        self.apples_points = {
            (2, 14), (8, 8), (11, 0), (5, 14),
            (12, 0), (11, 3), (6, 6), (13, 0),
            (2, 3), (3, 3), (11, 15), (2, 5),
            (1, 0), (11, 14)
        }

        self.snake = Snake(start_points=[(1, 1), (1, 2)])
        self.field = Field(snake=self.snake)

        for x, y in self.apples_points:
            self.field.field[x][y].content = Cell.apple

        self.game = GameManager(
            snake=self.snake,
            field=self.field,
        )

    def test_logs(self):
        """Тест метода logs класса GameManager"""
        for event, direction in self.iter_key:
            self.game.session['iter_key'].append(
                (event, deepcopy(direction))
            )
            self.game._GameManager__set_direction(direction)
            self.game.field.move_snake(direction)

        self.game.logs(filename='test_logs')

        self.assertTrue(os.path.exists(self.game.logs_dir))
        self.assertTrue(
            f'{os.path.exists(self.game.logs_dir)}/test_logs.pkl'
        )

        with open(f'{self.game.logs_dir}/test_logs.pkl', 'rb') as file:
            session = pickle.load(file)

        for row_log, row in zip(
                session['field'].field,
                self.game.session['field'].field
        ):
            for cell_log, cell in zip(row_log, row):
                self.assertTrue(cell_log.content == cell.content)

        self.assertTrue(
            session['delay'] == self.game.session['delay']
        )

        for pack_log, pack in zip(
            session['iter_key'],
            self.game.session['iter_key']
        ):
            _, d_log = pack_log
            _, d = pack

            self.assertTrue(d_log == d)

        os.remove(f'{self.game.logs_dir}/test_logs.pkl')

    def test_create_lvl(self):
        pass

if __name__ == '__main__':
    unittest.main()
