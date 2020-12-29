import unittest

from BugFile.maximum.maximum import maximum


class TestMaximum(unittest.TestCase):

    def test_1(self):
        assert maximum(3, 3, 5) == 5  # Passes
        assert maximum(1, 2, 3) == 3  # Passes


if __name__ == '__main__':
    unittest.main()
