import unittest

from Stores.Hole import Hole
from Stores.PatchStore import PatchStore
from Stores.ValidPatchStore import ValidPatchStore


class TestValidPatchStore(unittest.TestCase):
    """
    Tests the Patch.py script in the Stores.PatchStore
    """

    def test_add_valid_patches(self):
        """
        At first there are created patches and added in the patch store. Then they are added in the valid patch store.
        If there are found valid patches then the testsuite is successful.
        """
        ValidPatchStore.clear_valid_patch_list()
        PatchStore.clear_current_patch()
        sketch_name = "sketch_name2"
        test_name = "test_name2"
        PatchStore.set_current_sketch_and_test(sketch_name, test_name)

        hole = Hole(2, 100, ["f"], "EXP", 1)
        PatchStore.add_hole_to_patch(hole)

        hole = Hole(3, 49, ["d"], "EXP", 2)
        PatchStore.add_hole_to_patch(hole)

        ValidPatchStore.add_valid_patch(PatchStore.current_patch)
        self.assertTrue(ValidPatchStore.has_found_valid_patches())
        array = []
        for valid_patch in ValidPatchStore.valid_patch_list:
            array.append(valid_patch.to_array())
        self.assertEqual("[['sketch_name2', 'test_name2', [[2, 100, ['f'], 'EXP'], [3, 49, ['d'], 'EXP']]]]",
                         str(array))

    def test_add_valid_patches_different_sketches(self):
        """
        At first there are created patches and added in the patch store. Then they are added in the valid patch store.
        If there are found valid patches then the testsuite is successful. This is done twice with different kind of patches.
        """
        PatchStore.clear_current_patch()
        ValidPatchStore.clear_valid_patch_list()
        sketch_name = "sketch_name3"
        test_name = "test_name3"
        PatchStore.set_current_sketch_and_test(sketch_name, test_name)

        hole = Hole(2, 100, ["c"], "EXP", 1)
        PatchStore.add_hole_to_patch(hole)

        hole = Hole(3, 49, ["d"], "EXP", 2)
        PatchStore.add_hole_to_patch(hole)

        ValidPatchStore.add_valid_patch(PatchStore.current_patch)
        PatchStore.clear_current_patch()

        sketch_name = "sketch_name4"
        test_name = "test_name4"
        PatchStore.set_current_sketch_and_test(sketch_name, test_name)

        hole = Hole(5, 10, ["c + d"], "ARI", 1)
        PatchStore.add_hole_to_patch(hole)

        hole = Hole(7, 49, ["d - f"], "ARI", 2)
        PatchStore.add_hole_to_patch(hole)

        ValidPatchStore.add_valid_patch(PatchStore.current_patch)
        PatchStore.clear_current_patch()

        self.assertTrue(ValidPatchStore.has_found_valid_patches())
        array = []
        for valid_patch in ValidPatchStore.valid_patch_list:
            array.append(valid_patch.to_array())
        self.assertEqual(str(array),
                         "[['sketch_name3', 'test_name3', [[2, 100, ['c'], 'EXP'], [3, 49, ['d'], 'EXP']]], "
                         "['sketch_name4', 'test_name4', [[5, 10, ['c + d'], 'ARI'], [7, 49, ['d - f'], 'ARI']]]]")
        ValidPatchStore.clear_valid_patch_list()
        self.assertFalse(ValidPatchStore.has_found_valid_patches())

    def test_add_same_patches_for_same_sketch(self):
        """
        Tests if only one patch is added if the same patch is already in the store.
        """
        PatchStore.clear_current_patch()
        ValidPatchStore.clear_valid_patch_list()
        sketch_name = "sketch_name6"
        test_name = "test_name6"
        PatchStore.set_current_sketch_and_test(sketch_name, test_name)

        hole = Hole(2, 100, ["c"], "EXP", 1)
        PatchStore.add_hole_to_patch(hole)

        hole = Hole(3, 49, ["d"], "EXP", 2)
        PatchStore.add_hole_to_patch(hole)

        ValidPatchStore.add_valid_patch(PatchStore.current_patch)
        self.assertTrue(ValidPatchStore.has_found_valid_patches())
        ValidPatchStore.add_valid_patch(PatchStore.current_patch)
        array = []
        for valid_patch in ValidPatchStore.valid_patch_list:
            array.append(valid_patch.to_array())
        self.assertEqual(str(array),
                         "[['sketch_name6', 'test_name6', [[2, 100, ['c'], 'EXP'], [3, 49, ['d'], 'EXP']]]]")


if __name__ == '__main__':
    unittest.main()
