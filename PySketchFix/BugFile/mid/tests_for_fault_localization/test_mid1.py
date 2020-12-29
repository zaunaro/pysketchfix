import unittest

from BugFile.mid.mid import mid


class TestMid(unittest.TestCase):

    def test_1(self):
        assert mid(2, 1, 3) == 2  # Fails
        assert mid(3, 3, 5) == 3  # Passes


if __name__ == '__main__':
    unittest.main()
