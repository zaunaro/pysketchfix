import unittest

from Stores.Hole import Hole
from Stores.Patch import Patch
from Stores.PatchWriter import FinalPatchStore


class TestPatchWriter(unittest.TestCase):
    """
    Tests the PatchWriter.py script in the Stores.PatchWriter
    """

    def test_patch(self):
        """
        Test to add multiple patches in the final patch store in the patch writer.
        """
        hole1 = Hole(1, 100, ["a == b"], "ARI", '==')
        hole2 = Hole(2, 100, ["c and d"], "LOG", 'and')
        hole3 = Hole(3, 100, ["e + f"], "ARI", '+')
        hole4 = Hole(4, 100, ["g + h"], "ARI", '+')
        hole5 = Hole(5, 100, ["i - j"], "ARI", '-')

        # Sketch 1
        # Patch 1
        patch1 = Patch("sketchName1", "test1")
        patch1.add_hole(hole1)
        # Patch 2
        patch2 = Patch("sketchName1", "test1")
        patch2.add_hole(hole2)
        patch2.add_hole(hole3)
        valid_patches1 = [patch1, patch2]

        # Add the patches to the PatchWriter's FinalPatchStore.
        FinalPatchStore.collect_patches(valid_patches1)
        self.assertEqual(FinalPatchStore.number_of_total_patches, 2)
        self.assertEqual(FinalPatchStore.number_of_duplicate_patches, 0)
        # Check the counter
        for collection in FinalPatchStore.patch_collection:
            patch = collection[0]
            counter = collection[1]
            if patch.is_equal(patch1):
                self.assertEqual(counter, 1)
            if patch.is_equal(patch2):
                self.assertEqual(counter, 1)
        FinalPatchStore.collect_patches(valid_patches1)
        self.assertEqual(FinalPatchStore.number_of_total_patches, 2)
        self.assertEqual(FinalPatchStore.number_of_duplicate_patches, 2)
        # Check the counter
        for collection in FinalPatchStore.patch_collection:
            patch = collection[0]
            counter = collection[1]
            if patch.is_equal(patch1):
                print("Patch1")
                print(counter)
                self.assertEqual(counter, 2)
            if patch.is_equal(patch2):
                print("Patch2")
                print(counter)
                self.assertEqual(counter, 2)

        # Sketch 2
        # Patch 1 has hole 2 equal to patch 2.
        patch3 = Patch("sketchName2", "test2")
        patch3.add_hole(hole2)
        # Patch 1 has one hole equal to patch 1
        patch4 = Patch("sketchName2", "test2")
        patch4.add_hole(hole1)
        patch4.add_hole(hole4)
        patch4.add_hole(hole5)
        valid_patches2 = [patch3, patch4]
        FinalPatchStore.collect_patches(valid_patches2)
        self.assertEqual(FinalPatchStore.number_of_total_patches, 4)
        self.assertEqual(FinalPatchStore.number_of_duplicate_patches, 2)
        # Check the counter
        for collection in FinalPatchStore.patch_collection:
            patch = collection[0]
            counter = collection[1]
            if patch.is_equal(patch1):
                print("Patch1")
                print(counter)
                self.assertEqual(counter, 2)
            if patch.is_equal(patch2):
                print("Patch1")
                print(counter)
                self.assertEqual(counter, 2)
            if patch.is_equal(patch3):
                print("Patch3")
                print(counter)
                self.assertEqual(counter, 1)
            if patch.is_equal(patch4):
                print("Patch4")
                print(counter)
                self.assertEqual(counter, 1)


if __name__ == '__main__':
    unittest.main()
