import unittest
from src.functions import Functions

class TestMain(unittest.TestCase):
    def test_add(self):
        self.assertEqual(Functions.add(2, 3), 5)
        self.assertEqual(Functions.add(-1, 1), 0)

    def test_subtract(self):
        self.assertEqual(Functions.subtract(10, 4), 6)
        self.assertEqual(Functions.subtract(4, 10), -6)

    def test_multiply(self):
        self.assertEqual(Functions.multiply(7, 6), 42)
        self.assertEqual(Functions.multiply(0, 5), 0)

    def test_divide(self):
        self.assertEqual(Functions.divide(8, 2), 4.0)
        with self.assertRaises(ValueError):
            Functions.divide(8, 0)

    def test_max_value(self):
        self.assertEqual(Functions.max_value(5, 9), 9)
        self.assertEqual(Functions.max_value(-1, -5), -1)

    def test_min_value(self):
        self.assertEqual(Functions.min_value(3, 7), 3)
        self.assertEqual(Functions.min_value(-3, -7), -7)

    def test_power(self):
        self.assertEqual(Functions.power(2, 3), 8)
        self.assertEqual(Functions.power(5, 0), 1)

    def test_mod(self):
        self.assertEqual(Functions.mod(10, 3), 1)
        with self.assertRaises(ValueError):
            Functions.mod(10, 0)


if __name__ == "__main__":
    unittest.main()