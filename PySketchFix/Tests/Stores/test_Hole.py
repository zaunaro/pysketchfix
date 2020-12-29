import unittest

from Stores.Hole import Hole


class TestHole(unittest.TestCase):
    """
    Tests the Hole.py script in the Stores.Hole
    """

    def test_equal_hole(self):
        """
        Tests if two holes are equal, when every attribute is equal.
        """
        hole1 = Hole(2, 100, ["c"], "EXP", 1)
        hole2 = Hole(2, 100, ["c"], "EXP", 1)
        self.assertTrue(hole1.is_equal(hole2))
        self.assertTrue(hole2.is_equal(hole1))

    def test_different_value(self):
        """
        Tests if two holes are equal, when their value is different.
        """
        hole1 = Hole(2, 100, ["c"], "EXP", 1)
        hole2 = Hole(2, 100, ["c"], "EXP", 2)
        self.assertFalse(hole1.is_equal(hole2))
        self.assertFalse(hole2.is_equal(hole1))

    def test_different_value_but_is_equal(self):
        """
        Tests that two holes are equal with the has changed code method, when their value is different.
        """
        hole1 = Hole(2, 100, ["c"], "EXP", 1)
        hole2 = Hole(2, 100, ["c"], "EXP", 2)
        self.assertTrue(hole1.has_equal_changed_code(hole2))
        self.assertTrue(hole2.has_equal_changed_code(hole1))

    def test_different_line(self):
        """
        Tests if two holes are equal, when their line is different.
        """
        hole1 = Hole(1, 100, ["c"], "EXP", 2)
        hole2 = Hole(2, 100, ["c"], "EXP", 2)
        self.assertFalse(hole1.is_equal(hole2))
        self.assertFalse(hole2.is_equal(hole1))

    def test_different_hole_number(self):
        """
        Tests if two holes are equal, when their hole number is different.
        """
        hole1 = Hole(1, 99, ["c"], "EXP", 2)
        hole2 = Hole(1, 100, ["c"], "EXP", 2)
        self.assertFalse(hole1.is_equal(hole2))
        self.assertFalse(hole2.is_equal(hole1))

    def test_different_line_value(self):
        """
        Tests if two holes are equal, when their value and line is different.
        """
        hole1 = Hole(1, 100, ["c"], "EXP", 1)
        hole2 = Hole(2, 100, ["c"], "EXP", 2)
        self.assertFalse(hole1.is_equal(hole2))
        self.assertFalse(hole2.is_equal(hole1))

    def test_different_line_hole_number(self):
        """
        Tests if two holes are equal, when their line and hole number is different.
        """
        hole1 = Hole(1, 99, ["c"], "EXP", 1)
        hole2 = Hole(2, 100, ["c"], "EXP", 1)
        self.assertFalse(hole1.is_equal(hole2))
        self.assertFalse(hole2.is_equal(hole1))

    def test_different_value_hole_number(self):
        """
        Tests if two holes are equal, when their value and hole number is different.
        """
        hole1 = Hole(1, 99, ["c"], "EXP", 1)
        hole2 = Hole(1, 100, ["c"], "EXP", 2)
        self.assertFalse(hole1.is_equal(hole2))
        self.assertFalse(hole2.is_equal(hole1))

    def test_different_code(self):
        """
        Tests if two holes are equal, when their code array has a different content.
        """
        hole1 = Hole(1, 100, ["c"], "EXP", 2)
        hole2 = Hole(1, 100, ["d"], "ARI", 2)
        self.assertFalse(hole1.is_equal(hole2))
        self.assertFalse(hole2.is_equal(hole1))

    def test_different_code_with_bigger_array(self):
        """
        Tests if two holes are equal, when their code array has a bigger content.
        """
        hole1 = Hole(1, 100, ["c", "d"], "EXP", 2)
        hole2 = Hole(1, 100, ["c", "e", "d"], "EXP", 2)
        self.assertFalse(hole1.is_equal(hole2))
        self.assertFalse(hole2.is_equal(hole1))

    def test_different_code_with_variation(self):
        """
        Tests if two holes are equal, when their code array has a different content.
        """
        hole1 = Hole(1, 100, ["c==d", "d==a"], "ARI", 2)
        hole2 = Hole(1, 100, ["c==d", "e==a"], "ARI", 2)
        self.assertFalse(hole1.is_equal(hole2))
        self.assertFalse(hole2.is_equal(hole1))

    def test_different_code_line_value(self):
        """
        Tests if two holes are equal, when their code array, the line and the value have different content.
        """
        hole1 = Hole(1, 100, ["c==d", "d==a"], "ARI", 2)
        hole2 = Hole(2, 100, ["c==d", "e==a"], "ARI", 1)
        self.assertFalse(hole1.is_equal(hole2))
        self.assertFalse(hole2.is_equal(hole1))

    def test_equal_code_with_variation(self):
        """
        Tests if two holes are equal, when their code array has the same content but on different positions.
        """
        hole1 = Hole(1, 100, ["c==d", "d==c", "a==b", "b==a"], "ARI", 2)
        hole2 = Hole(1, 100, ["b==a", "d==c", "c==d", "a==b"], "ARI", 2)
        self.assertTrue(hole1.is_equal(hole2))
        self.assertTrue(hole2.is_equal(hole1))


if __name__ == '__main__':
    unittest.main()
