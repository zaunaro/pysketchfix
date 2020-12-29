import unittest

from BugFile.mid.mid import mid


class TestMid(unittest.TestCase):

    def test_2(self):
        assert mid(1, 2, 3) == 2  # Passes
        assert mid(5, 5, 5) == 5  # Passes


if __name__ == '__main__':
    unittest.main()
