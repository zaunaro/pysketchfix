import unittest
from Stores.Hole import Hole
from Stores.Patch import Patch


class TestPatch(unittest.TestCase):
    """
    Tests the Patch.py script in the Stores.Patch
    """

    def test_patch_add_hole(self):
        """
        Adds a hole to a patch and looks if it is in the array.
        """
        patch1 = Patch("sketchName1", "test1")
        hole1 = Hole(1, 100, ["d==a"], "ARI", 2)
        patch1.add_hole(hole1)
        for hole in patch1.holes:
            self.assertTrue(hole.is_equal(hole1))
            break

    def test_patch_add_equal_holes(self):
        """
        Adds a hole to a patch and then the same hole again. The testsuite passes if an error occurs.
        """
        patch2 = Patch("sketchName2", "test2")
        hole2 = Hole(1, 100, ["d==a"], "ARI", 2)
        patch2.add_hole(hole2)
        has_Error = False
        try:
            patch2.add_hole(hole2)
        except RuntimeError:
            has_Error = True
        self.assertTrue(has_Error)

    def test_patch_add_different_holes(self):
        """
        Adds a hole to a patch and then a different hole. The testsuite passes if both holes are in the array.
        """
        patch3 = Patch("sketchName3", "test3")
        hole3 = Hole(1, 100, ["d==a"], "ARI", 2)
        patch3.add_hole(hole3)
        hole4 = Hole(2, 100, ["e==a"], "ARI", 2)
        patch3.add_hole(hole4)
        self.assertTrue(len(patch3.holes) == 2)

    def test_equal_patches(self):
        """
        Tests if two patches are equal (with the same holes).
        """
        patch4 = Patch("sketchName4", "test4")
        hole4 = Hole(1, 100, ["d==a"], "ARI", 2)
        patch4.add_hole(hole4)
        hole5 = Hole(2, 100, ["e==a"], "ARI", 2)
        patch4.add_hole(hole5)
        patch5 = Patch("sketchName4", "test4")
        patch5.add_hole(hole4)
        patch5.add_hole(hole5)
        self.assertTrue(patch4.is_equal(patch5))
        self.assertTrue(patch5.is_equal(patch4))

    def test_different_patches_from_equal_tests(self):
        """
        Tests if two patches are different with different sketch names.
        """
        hole6 = Hole(2, 100, ["e==a"], "ARI", 2)
        patch6 = Patch("sketchName6", "test6")
        patch6.add_hole(hole6)
        patch7 = Patch("sketchName7", "test6")
        patch7.add_hole(hole6)
        self.assertFalse(patch6.is_equal(patch7))
        self.assertFalse(patch7.is_equal(patch6))

    def test_different_patches_from_equal_sketches(self):
        """
        Tests if two patches are different with different testsuite names.
        """
        hole7 = Hole(2, 100, ["e==a"], "ARI", 2)
        patch8 = Patch("sketchName8", "test8")
        patch8.add_hole(hole7)
        patch9 = Patch("sketchName8", "test9")
        patch9.add_hole(hole7)
        self.assertFalse(patch8.is_equal(patch9))
        self.assertFalse(patch9.is_equal(patch8))

    def test_different_patches(self):
        """
        Tests if two patches are different (with the different holes).
        """
        patch10 = Patch("sketchName10", "test10")
        hole8 = Hole(1, 100, ["d==a"], "ARI", 2)
        patch10.add_hole(hole8)
        hole9 = Hole(2, 100, ["e==a"], "ARI", 2)
        patch10.add_hole(hole9)
        patch11 = Patch("sketchName10", "test10")
        hole10 = Hole(1, 100, ["e==d"], "ARI", 2)
        patch11.add_hole(hole10)
        hole11 = Hole(2, 100, ["e==a"], "ARI", 2)
        patch11.add_hole(hole11)
        self.assertFalse(patch10.is_equal(patch11))
        self.assertFalse(patch10.is_equal(patch11))


if __name__ == '__main__':
    unittest.main()
