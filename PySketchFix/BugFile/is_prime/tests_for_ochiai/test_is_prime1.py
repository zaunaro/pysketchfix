import unittest

from BugFile.is_prime.is_prime import is_prime


class TestMaximum(unittest.TestCase):

    def test_1(self):
        self.assertEqual(is_prime(3), True)  # Passes
        self.assertEqual(is_prime(2), True)  # Passes


if __name__ == '__main__':
    unittest.main()
