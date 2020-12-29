class ValidPatchStore:
    """
    The valid patch store stores a list of patches. All of them pass at least one testsuite with the current sketch.
    This list is cleared after every sketch.
    """
    valid_patch_list = []

    @staticmethod
    def has_found_valid_patches():
        """
        :return: True, if there are any patches in this store, false otherwise.
        """
        return len(ValidPatchStore.valid_patch_list) > 0

    @staticmethod
    def clear_valid_patch_list():
        """
        Clears all patches in the store. This is done after every sketch.
        """
        ValidPatchStore.valid_patch_list = []

    @staticmethod
    def add_valid_patch(new_patch):
        """
        Checks if the patch is already in the store, if it is not in the store it is added to the list.

        :param new_patch: The new patch which is added into the list in the store.
        :return: True, if the patch is added, false if it is a duplicate.
        """
        for valid_patch in ValidPatchStore.valid_patch_list:
            if valid_patch.is_equal(new_patch):
                return False
        ValidPatchStore.valid_patch_list.append(new_patch)
        return True
