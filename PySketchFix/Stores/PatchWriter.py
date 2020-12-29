from Config import FileHandler
from Config.ConfigReader import ConfigReader


def print_non_reaching_hole_sketch(current_sketch_basename):
    """
    If the testsuite is successful but the valid patch store has no patches in it, then no hole is reached and
    the testsuite passes. The sketch is useless because no hole is reached with the testsuite.

    :param current_sketch_basename: The sketch which is executed at the moment with his .py annotation.
    """
    FinalPatchStore.increment_number_of_non_reaching_holes_sketches()
    print(FinalPatchStore.TABLE)
    print('\t\t0' + '\t\t\t\t' + '⚠' + '\t\t\t' + str(current_sketch_basename))


def print_failing_sketch(current_sketch_basename):
    """
    If the testsuite fails every time while execution and no patch could be found for this sketch. This testsuite is
    marked as failing.

    :param current_sketch_basename: The sketch which is executed at the moment with his .py annotation.
    """
    FinalPatchStore.increment_number_of_failing_sketches()
    print(FinalPatchStore.TABLE)
    print('\t\t0' + '\t\t\t\t' + 'x' + '\t\t\t' + str(current_sketch_basename))


def print_and_write_passing_sketch(current_sketch_basename, valid_patches):
    """
    If the testsuite fails passes and a patch could be found for this sketch. This testsuite is marked as passing. The
    valid patches of the valid patch store are taken und written into patch output files.

    :param current_sketch_basename: The sketch which is executed at the moment with his .py annotation.
    :param valid_patches: The valid patches of the valid patch store.
    """
    # Increment the number of passing sketches in the final patch store and add the patches of the list.
    FinalPatchStore.increment_number_of_passing_sketches()
    FinalPatchStore.collect_patches(valid_patches)
    number_of_patches = len(valid_patches)
    print(FinalPatchStore.TABLE)
    print(str(number_of_patches) + '\t\t\t\t' + '✓' + '\t\t\t' + str(current_sketch_basename))

    # Only if the parameter is true, then patches for each sketch (where patches are found are printed)
    counter = 0
    content = ''
    PRINT_PATCHES_FOR_EACH_SKETCH = bool(ConfigReader.get_print_for_every_sketch_parameter())
    PATCH_DIRECTORY = ConfigReader.get_patch_directory()
    if PRINT_PATCHES_FOR_EACH_SKETCH:
        for valid_patch in valid_patches:
            counter += 1
            content += FinalPatchStore.SEP + "\n"
            content += "Patch " + str(counter) + "\n"
            content += str(valid_patch.to_patch_format()) + "\n"
        FileHandler.write_patch_file(str(current_sketch_basename) + ".txt", content, PATCH_DIRECTORY)


def print_and_write_total_patches():
    """
    At the end the total number of passing sketches are printed and a final file is created where all patches with holes
    are listed.
    """
    print("Sketches:")
    print("Number of sketches where patches are found: " + str(FinalPatchStore.number_of_passing_sketches))
    print("Number of sketches where no patch could be found and the testsuite still fails: " + str(
        FinalPatchStore.number_of_failing_sketches))
    print("Number of sketches where no patch could be found but the testsuite is passing: " + str(
        FinalPatchStore.number_of_non_reaching_holes_sketches))
    if float(FinalPatchStore.number_of_total_sketches) == 0:
        print("Percentage of successful sketches: 0%")
    else:
        print("Percentage of successful sketches: " + str(
            round(float(FinalPatchStore.number_of_passing_sketches) / float(
                FinalPatchStore.number_of_total_sketches) * 100,
                  2)) + "%")
    print(FinalPatchStore.SEP)

    print("Patches:")
    print("Number of (non duplicate) created patches: " + str(FinalPatchStore.number_of_total_patches))
    print("Number of duplicate created patches: " + str(FinalPatchStore.number_of_duplicate_patches))
    print("Number of total created patches: " + str(
        FinalPatchStore.number_of_duplicate_patches + FinalPatchStore.number_of_total_patches))
    if FinalPatchStore.number_of_total_patches > 0:
        print("Percentage of duplicates: " + str(round(float(FinalPatchStore.number_of_duplicate_patches) / (float(
            FinalPatchStore.number_of_duplicate_patches) + float(FinalPatchStore.number_of_total_patches)) * 100,
                                                       2)) + "%")
    else:
        print("Percentage of duplicates: 0%")
    print(FinalPatchStore.SEP)

    print("Look at the output file '_patches_with_holes.txt' in the patches folder to get the holes of the " +
          "patches created.")

    # Write all patches without duplicates in one final file.
    patch_counter = 0
    content = ''
    PATCH_DIRECTORY = ConfigReader.get_patch_directory()
    for collection in FinalPatchStore.patch_collection:
        patch_counter += 1
        # Fetch the counter and the patch.
        patch = collection[0]
        counter = collection[1]

        # Set the content with the patch number and how many times the patch appears.
        content += FinalPatchStore.SEP + "\n"
        content += "Patch " + str(patch_counter) + "\n" + "Counter: " + str(counter) + "\n"
        content += str(patch.to_patch_format()) + "\n"

    FileHandler.write_patch_file("_patches_with_holes.txt", content, PATCH_DIRECTORY)


class FinalPatchStore:
    """
    The FinalPatchStore holds the information about created, passing and failing sketches. This is stored to get the
    statistics of the execution at the end. Here also the output files for the patches are created.
    """
    SEP = "-------------------------------------------------------------------------------------------------------"
    TABLE = " Number of patches | Test Result | ✎ Sketch"
    number_of_total_sketches = 0
    number_of_passing_sketches = 0
    number_of_failing_sketches = 0
    number_of_non_reaching_holes_sketches = 0
    patch_collection = []
    number_of_total_patches = 0
    number_of_duplicate_patches = 0

    @staticmethod
    def increment_number_of_failing_sketches():
        """
        Increment the number of sketches which fail the testsuite and the number of total sketches.
        """
        FinalPatchStore.number_of_failing_sketches += 1
        FinalPatchStore.number_of_total_sketches += 1

    @staticmethod
    def increment_number_of_passing_sketches():
        """
        Increment the number of sketches which pass the testsuite and the number of total sketches.
        """
        FinalPatchStore.number_of_passing_sketches += 1
        FinalPatchStore.number_of_total_sketches += 1

    @staticmethod
    def increment_number_of_non_reaching_holes_sketches():
        """
        Increment the number of sketches which do not reach any holes and the testsuite is successful and the number of
        total sketches.
        """
        FinalPatchStore.number_of_non_reaching_holes_sketches += 1
        FinalPatchStore.number_of_total_sketches += 1

    @staticmethod
    def collect_patches(valid_patch_list):
        """
        The patch collection stores a tuple of valid patch holes and the number of how many times the hole is found.
        This number gets incremented as soon as the hole is found again.

        :param valid_patch_list: The valid patches of the passing sketches.
        """
        # If the collection is empty then every patch in the valid patch list gets appended, because the valid patch
        # list is also free of duplicates.
        if len(FinalPatchStore.patch_collection) == 0:
            for new_patch in valid_patch_list:
                FinalPatchStore.patch_collection.append([new_patch, 1])
                FinalPatchStore.number_of_total_patches += 1
        else:
            # Now for every patch in the list check if the patch is already in the collection.
            for new_patch in valid_patch_list:
                is_duplicate_patch = False
                for collection in FinalPatchStore.patch_collection:
                    # Fetch the counter and the patch.
                    patch = collection[0]
                    counter = collection[1]

                    # Check if the patch is equal to the new patch. If so, then the flag is true and the counter gets
                    # incremented.
                    if patch.has_equal_holes(new_patch):
                        is_duplicate_patch = True
                        counter += 1
                        collection[1] = counter
                        FinalPatchStore.number_of_duplicate_patches += 1
                        break

                # If the flag is not set then add the patch with the counter to the collection.
                if not is_duplicate_patch:
                    FinalPatchStore.patch_collection.append([new_patch, 1])
                    FinalPatchStore.number_of_total_patches += 1
