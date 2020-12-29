import unittest

from BugFile.maximum.maximum import maximum


class TestMaximum(unittest.TestCase):

    def test_1(self):
        assert maximum(3, 3, 5) == 5  # Passes
        assert maximum(1, 2, 3) == 3  # Passes

    def test_2(self):
        assert maximum(3, 2, 1) == 3  # Passes
        assert maximum(5, 3, 4) == 5  # Passes

    def test_3(self):
        assert maximum(-2, -1, -3) == -1  # Fails
        assert maximum(5, 5, 5) == 5  # Passes


if __name__ == '__main__':
    unittest.main()
