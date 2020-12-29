import unittest

from BugFile.positive_indicator.positive_indicator import indicator


class TestIndicator(unittest.TestCase):
    def test_2(self):
        assert indicator(1, []) == False  # Fails
        assert indicator(2, [1, 2, 3, 4]) == True  # Passes


if __name__ == '__main__':
    unittest.main()
