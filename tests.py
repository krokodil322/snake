from objects import *

import unittest


class CellTest(unittest.TestCase):
    def setUp(self) -> None:
        self.cell = Cell()

    def test_attrs(self):
        self.assertTrue(
            all(
                hasattr(self.cell, attr) for attr in ('content', 'default')
            )
        )

    def test_default(self):
        self.assertTrue(self.cell.content == self.cell.default)

    def test_bool(self):
        self.assertFalse(self.cell)

        self.cell.content = '0'
        self.assertTrue(self.cell)


class FieldTest(unittest.TestCase):
    def setUp(self) -> None:
        self.field = Field()

    def test_set_into_cell(self):
        self.field.set_into_cell(8, 8, '0')
        self.assertTrue(
            self.field.field[8][8].content == '0'
        )



if __name__ == '__main__':
    unittest.main()
