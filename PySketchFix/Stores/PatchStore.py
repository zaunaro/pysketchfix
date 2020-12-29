from Stores.Patch import Patch


class PatchStore:
    """
    All transformation types have access to the patch store. The patch store contains valid and invalid holes. After
    every testsuite iteration (could be the same testsuite multiple times) the current patch is cleared. If the current
    patch contains holes (added by the transformations) it is taken and put into the valid patch store. To every patch
    the current sketch with is tested and the current testsuite which is tested at the moment is stored.
    """
    current_sketch_name = ""
    current_test_name = ""
    current_patch = None

    @staticmethod
    def set_current_sketch_and_test(sketch_name, test_name):
        """
        Set the current sketch and testsuite which were executed and reset the current patch.

        :param sketch_name: The sketch which is tested at the moment. (Sketch name without .py and path)
        :param test_name: The testsuite which is executed at the moment. (Tests name without .py and path)
        """
        PatchStore.current_sketch_name = sketch_name
        PatchStore.current_test_name = test_name
        PatchStore.clear_current_patch()

    @staticmethod
    def add_hole_to_patch(hole):
        """
        Every transformation type has access to this method. If the testsuite execution reaches a hole then a patch is
        created. If a patch is already created while this iteration, then add the hole in the current patch.

        :param hole: The hole which is added to the patch.
        :raise: RuntimeError, if the current sketch and testsuite name is empty.
        """
        if PatchStore.current_sketch_name == "" or PatchStore.current_test_name == "":
            raise RuntimeError("No sketch and testsuite name is set, to insert the hole: " + str(hole.to_array()))
        if PatchStore.current_patch is None:
            PatchStore.current_patch = Patch(PatchStore.current_sketch_name, PatchStore.current_test_name)
            PatchStore.current_patch.add_hole(hole)
        else:
            PatchStore.current_patch.add_hole(hole)

    @staticmethod
    def clear_current_patch():
        """
        Clear the current patch after every testsuite iteration.
        """
        PatchStore.current_patch = None
