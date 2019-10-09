import unittest
from source.main import num_check


class TestMethods(unittest.TestCase):
    # num_check from main
    def test_num_check(self):
        # Arrange
        fixtures = [
            {"test_num": "1", "int_max": 10, "expected": 1},
            {"test_num": "10", "int_max": 10, "expected": 10},
            {"test_num": "-1", "int_max": 10, "expected": -1},
            {"test_num": "11", "int_max": 10, "expected": -1},
            {"test_num": "5.5", "int_max": 10, "expected": -2},
            {"test_num": "mice", "int_max": 10, "expected": -2}
        ]

        for fixture in fixtures:
            # Act
            actual = num_check(fixture["test_num"], fixture["int_max"])
            # Assert
            self.assertEqual(actual, fixture["expected"])


if __name__ == '__main__':
    unittest.main()
