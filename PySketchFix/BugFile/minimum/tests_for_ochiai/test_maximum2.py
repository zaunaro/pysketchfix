import unittest

from BugFile.maximum.maximum import maximum


class TestMaximum(unittest.TestCase):

    def test_2(self):
        assert maximum(3, 2, 1) == 3  # Passes
        assert maximum(5, 3, 4) == 5  # Passes


if __name__ == '__main__':
    unittest.main()
