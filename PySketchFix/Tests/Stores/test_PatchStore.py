import unittest

from Stores.Hole import Hole
from Stores.PatchStore import PatchStore


class TestPatchStore(unittest.TestCase):
    """
    Tests the Patch.py script in the Stores.PatchStore
    """

    def test_current_sketch_and_test(self):
        """
        First is checked if an exception is raised when sketch and testsuite name are not set.
        Sets the current sketch and testsuite and testsuite if they are equal and the current patch is none.
        """
        PatchStore.clear_current_patch()
        PatchStore.set_current_sketch_and_test("", "")
        hole1 = Hole(2, 100, ["c"], "EXP", 1)
        has_error = False
        try:
            PatchStore.add_hole_to_patch(hole1)
        except RuntimeError:
            has_error = True
        self.assertTrue(has_error)

        sketch_name = "sketch_name1"
        test_name = "test_name1"
        PatchStore.set_current_sketch_and_test(sketch_name, test_name)
        self.assertEqual(PatchStore.current_sketch_name, sketch_name)
        self.assertEqual(PatchStore.current_test_name, test_name)
        self.assertTrue(PatchStore.current_patch is None)

        sketch_name = "sketch_name2"
        test_name = "test_name2"
        PatchStore.set_current_sketch_and_test(sketch_name, test_name)
        self.assertEqual(PatchStore.current_sketch_name, sketch_name)
        self.assertEqual(PatchStore.current_test_name, test_name)
        self.assertTrue(PatchStore.current_patch is None)

    def test_add_hole_to_patch(self):
        """
        Adds a hole to a patch. If the current patch is none then it is a new one created otherwise the current patch
        is taken to add the hole. If a hole is added twice in one patch then a new error is thrown.
        """
        hole1 = Hole(2, 100, ["c"], "EXP", 1)
        hole2 = Hole(3, 49, ["d"], "EXP", 2)
        sketch_name = "sketch_name1"
        test_name = "test_name1"
        PatchStore.set_current_sketch_and_test(sketch_name, test_name)
        PatchStore.add_hole_to_patch(hole1)
        self.assertTrue(PatchStore.current_patch is not None)
        array = PatchStore.current_patch.to_array()
        self.assertEqual("['sketch_name1', 'test_name1', [[2, 100, ['c'], 'EXP']]]", str(array))
        has_error = False
        try:
            PatchStore.add_hole_to_patch(hole1)
        except RuntimeError:
            has_error = True
        self.assertTrue(has_error)
        PatchStore.add_hole_to_patch(hole2)
        array = PatchStore.current_patch.to_array()
        self.assertEqual("['sketch_name1', 'test_name1', [[2, 100, ['c'], 'EXP'], [3, 49, ['d'], 'EXP']]]", str(array))
        PatchStore.clear_current_patch()
        self.assertTrue(PatchStore.current_patch is None)


if __name__ == '__main__':
    unittest.main()
