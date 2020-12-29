import unittest

from BugFile.mid.mid import mid


class TestMid(unittest.TestCase):
    def test_1(self):
        assert mid(2, 1, 3) == 2 # Fails
        assert mid(3, 3, 5) == 3 # Passes

    def test_2(self):
        assert mid(1, 2, 3) == 2 # Passes
        assert mid(5, 5, 5) == 5 # Passes

    def test_3(self):
        assert mid(5, 3, 4) == 4 # Fails
        assert mid(3, 2, 1) == 2 # Passes


if __name__ == '__main__':
    unittest.main()
