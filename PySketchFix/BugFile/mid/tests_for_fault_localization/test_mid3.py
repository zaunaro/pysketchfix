import unittest

from BugFile.mid.mid import mid


class TestMid(unittest.TestCase):

    def test_3(self):
        assert mid(5, 3, 4) == 4 # Passes
        assert mid(3, 2, 1) == 2 # Passes


if __name__ == '__main__':
    unittest.main()
