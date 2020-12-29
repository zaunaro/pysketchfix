import unittest

from BugFile.maximum.maximum import maximum


class TestMaximum(unittest.TestCase):

    def test_3(self):
        assert maximum(-2, -1, -3) == -1  # Fails
        assert maximum(5, 5, 5) == 5  # Passes


if __name__ == '__main__':
    unittest.main()
