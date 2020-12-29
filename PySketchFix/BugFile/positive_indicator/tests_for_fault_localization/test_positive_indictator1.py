import unittest

from BugFile.positive_indicator.positive_indicator import indicator


class TestIndicator(unittest.TestCase):
    def test_1(self):
        assert indicator(1, [1, 2, 3]) == True  # Passes
        assert indicator(1, [0, 2, 3]) == False  # Fails


if __name__ == '__main__':
    unittest.main()
