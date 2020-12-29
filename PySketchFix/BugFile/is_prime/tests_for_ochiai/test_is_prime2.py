import unittest

from BugFile.is_prime.is_prime import is_prime


class TestMaximum(unittest.TestCase):

    def test_2(self):
        self.assertEqual(is_prime(4), False)  # Fails
        self.assertEqual(is_prime(8), False)  # Fails

if __name__ == '__main__':
    unittest.main()
