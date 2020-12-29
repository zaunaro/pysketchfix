import unittest

from BugFile.is_prime.is_prime import is_prime


class TestMaximum(unittest.TestCase):

    def test_1(self):
        self.assertEqual(is_prime(3), True)  # Passes
        self.assertEqual(is_prime(2), True)  # Passes

    def test_2(self):
        self.assertEqual(is_prime(4), False)  # Fails
        self.assertEqual(is_prime(8), False)  # Fails

    def test_3(self):
        self.assertEqual(is_prime(0), True)  # Passes
        self.assertEqual(is_prime(1), True)  # Passes


if __name__ == '__main__':
    unittest.main()
