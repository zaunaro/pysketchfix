import unittest

from BugFile.minimum.minimum import minimum


class TestMinimum(unittest.TestCase):

    def test_1(self):
        assert minimum(3, 3, 5) == 3  # Passes
        assert minimum(1, 2, 3) == 1  # Passes

    def test_2(self):
        assert minimum(3, 2, 1) == 1  # Fails
        assert minimum(5, 3, 4) == 3  # Passes

    def test_3(self):
        assert minimum(-2, -1, -3) == -3  # Fails
        assert minimum(5, 5, 5) == 5  # Passes


if __name__ == '__main__':
    unittest.main()
