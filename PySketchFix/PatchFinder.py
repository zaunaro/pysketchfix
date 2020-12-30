import os
import sys
import time

from Config import FileHandler
from Config.ConfigReader import ConfigReader
from Schemas.TransformationManager import TransformationManager
from Stores import PatchWriter
from Stores.PatchStore import PatchStore
from Stores.ValidPatchStore import ValidPatchStore


def run_sketches(bug_file, unit_test_file):
    """
    This method starts to testsuite the created sketches and decides with the tests_for_ochiai which of them is a valid
    patch or not.

    :param bug_file: The bug file where patches are find.
    :param unit_test_file: The unit testsuite suite file which tests_for_ochiai the bug file.
    :raise: RuntimeError: if the testsuite suite contains no failing testsuite case.
    """
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print()
    print("	                                     PyPatchFinder for Python®")
    print()
    print("                   ✓ = Passing, x = Failing, ⚠ = Passing without reaching hole")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    start_time = time.time()

    # Setup the Config directory with the two files which are taken as arguments. The one is the bug file and the
    # other one the unit testsuite file to it. It is also needed where the project is located, to store sketches and
    # patches right, so the project path is taken from this file.
    project_path = os.path.dirname(os.path.abspath(__file__))
    ConfigReader.setup_environment_for_PatchFinder(bug_file, unit_test_file, project_path)
    print("PySketchFix will run with:\nbug file: " + bug_file + "\nunit testsuite: " + unit_test_file)

    # Delete all recent created patches but not the cache and init files. Therefore the config parameter patch directory
    # is checked.
    PATCH_DIRECTORY = str(ConfigReader.get_patch_directory())
    for filename in os.listdir(PATCH_DIRECTORY):
        if not filename.__contains__("__pycache__") and not filename.__contains__("__init__"):
            os.remove(os.path.join(PATCH_DIRECTORY, filename))

    # Check the generated sketches and remove the __cache__ and __init__ files from the array so they won't be called
    # later while execution. Make sure that all sketch files of the array are python and not empty.
    SKETCH_DIRECTORY = str(ConfigReader.get_sketch_directory())
    sketches = os.listdir(SKETCH_DIRECTORY)
    sketches = remove_init_cache_files(sketches)
    check_type_of_sketch_files(sketches)

    # Before the tests_for_ochiai with the sketches are run, the original bug file should at first be executed to set
    # the number of failing tests_for_ochiai. Raise a RunTimeError if there are no failing tests_for_ochiai in the
    # testsuite suite.
    print("-------------------------------------------------------------------------------------------------------")
    print("                          Original Bug File " + str(ConfigReader.get_bug_file_basename()))
    NUMBER_OF_ORIGINAL_FAILING_TESTS = run_tests_with_current_bug_file("Original")
    if NUMBER_OF_ORIGINAL_FAILING_TESTS == 0:
        raise RuntimeError(
            "There are no failing tests_for_ochiai in the testsuite suite PySketchFix can only find patches if at "
            "least one failing testsuite case is in the unit testsuite suite.")

    # Now before the sketch testsuite execution starts the bug file is saved in a Backup folder to ensure nothing gets
    # deleted. This is because every sketch content is copied in the bug file and it is possible that an error occurs
    # and then the content of the bug file is loosed.
    BACKUP_BUG_FILE = ConfigReader.get_backup_bug_file()
    BUG_FILE = ConfigReader.get_bug_file()
    for current_sketch_basename in sketches:
        FileHandler.copy_bug_file_to_backups(BUG_FILE, BACKUP_BUG_FILE)
        print("-------------------------------------------------------------------------------------------------------")
        print("                          ✎ Sketch " + str(current_sketch_basename))
        # When the current sketch basename is changed with the bug file, then the testsuite is executed multiple times.
        # The method returns True, if at least one time the testsuite passes, false if it fails every time.
        # The try and catch block is needed, if an error in executions occurs. Then the bug file should be removed back
        # from the backups to save it and don't lose the content of it.
        try:
            run_sketch(current_sketch_basename, NUMBER_OF_ORIGINAL_FAILING_TESTS)
        finally:
            FileHandler.move_bug_file_from_backups(BUG_FILE, BACKUP_BUG_FILE)

    # At the end print the statistics for the whole execution.
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Execution successful:")
    PatchWriter.print_and_write_total_patches()
    print("--- %s minutes ---" % ((time.time() - start_time) / 60))
    print()


def remove_init_cache_files(list_of_sketches):
    """
    Remove the '__init__' and '__cache__' files if they were generated from PyCharm in the array. This is done because
    all sketches are copied and executed later. So to avoid execution of these files the are removed of the array.

    :param list_of_sketches: A list of sketches where init and cache is in it.
    :return: the list_of_files without init and cache files.
    """
    list_of_sketches_without_init_cache_file = []
    for file in list_of_sketches:
        if not str(file) == "__init__.py" and not str(file) == "__pycache__":
            list_of_sketches_without_init_cache_file.append(file)
    return list_of_sketches_without_init_cache_file


def check_type_of_sketch_files(list_of_sketches):
    """
    Check the files in the sketch directory, if they were Python type and also if the array is not empty at all.

    :param list_of_sketches: The list of generated sketches.
    :raise Exception if the array is empty or has one file which is not python.
    """
    if len(list_of_sketches) == 0:
        raise Exception("There are no files in the sketch directory.")

    for file in list_of_sketches:
        if not file.endswith('.py'):
            raise Exception("The file " + str(file) + " in the sketch directory is not Python.")


def run_tests_with_current_bug_file(sketch_name):
    """
    Run the current sketch with the bug file tests. Therefore the sketch is changed with the original bug file.
    The test result is stored in the PatchStore and the number of failures of this test execution is stored.

    :param sketch_name: The current sketch with which the original bug file is changed.
    :return: the number of failing tests_for_ochiai with the current bug file.
    """
    # Fetch the verbosity, unit testsuite file directory and the unit testsuite basename of the bug file and start
    # testing.
    UNIT_TEST_FILE_DIRECTORY = str(ConfigReader.get_unit_test_file_directory())
    UNIT_TEST_FILE_BASENAME = str(ConfigReader.get_unit_test_file_basename())
    # Set the current sketch and test and run the tests.
    PatchStore.set_current_sketch_and_test(sketch_name, UNIT_TEST_FILE_BASENAME)
    # Get the executor and the interpreter of the config directory.
    TESTRUNNER = ConfigReader.get_test_runner()
    PYTHON = ConfigReader.get_python_interpreter()
    # Start the test runner in a new environment. Here the output file is created.
    os.system(
        PYTHON + " " + TESTRUNNER + " " + UNIT_TEST_FILE_DIRECTORY + " " + UNIT_TEST_FILE_BASENAME + " " + sketch_name)
    # Get the errors of the output file and return it.
    errors = FileHandler.parse_test_output(UNIT_TEST_FILE_DIRECTORY, UNIT_TEST_FILE_BASENAME)
    return errors


def run_sketch(current_sketch_basename, number_of_original_failing_tests):
    """
    The current bug file was replaced with this sketch file. So now the testsuite can be executed and the search for the
    patches is started.

    :param number_of_original_failing_tests: the number of original failing tests_for_ochiai with the original bug file.
    :param current_sketch_basename: The sketch which is tested at the moment.
    """
    # Before there is the bug file content changed with the current sketch content.
    SKETCH_DIRECTORY = ConfigReader.get_sketch_directory()
    BUG_FILE = ConfigReader.get_bug_file()
    FileHandler.change_bug_file_with_sketch(BUG_FILE, current_sketch_basename, SKETCH_DIRECTORY)

    # Set the current testsuite and sketch which is executed at the moment in the patch store. This is needed to
    # identify the patch later.
    BUG_FILE_TEST = str(ConfigReader.get_unit_test_file())

    # The maximal iterations done to find a patch are set. This describes how many times the testsuite is executed.
    # If the number is very high, then more possible transformations can be done. The iterations which are successful
    # and not are successful are counted.
    MAX_ITERATIONS = ConfigReader.get_max_iterations()
    STRICT_PATCH_TREATMENT = ConfigReader.get_strict_patch_treatment()
    PatchStore.set_current_sketch_and_test(current_sketch_basename, BUG_FILE_TEST)
    iterations = 0
    non_successful_iterations = 0
    successful_iterations = 0
    while iterations < MAX_ITERATIONS:
        # Because the current sketch content is replaced with the bug file it can be run.
        iterations += 1

        # Now the tests_for_ochiai are run with the current bug file. Here the number of failing tests_for_ochiai is
        # returned.
        failing_tests = run_tests_with_current_bug_file(current_sketch_basename)

        # A testsuite is successful, if the number of original failing tests_for_ochiai is now equal or less then the
        # the current failing tests_for_ochiai. But if you set the strict patch treatment to true, then the number of
        # failing tests_for_ochiai must be 0.
        if STRICT_PATCH_TREATMENT:
            successful_test_execution = failing_tests == 0
        else:
            successful_test_execution = number_of_original_failing_tests > failing_tests

        # In the patch store, a current patch is stored where all hole transformations done in the execution are
        # stored. If this patch is none, then no holes are reached, but the testsuite is still successful.
        # If the current patch is not empty and there are hole transformations created in the execution.
        # Then the current patch is (if it is not in the valid patch store already) added to it.
        if successful_test_execution and PatchStore.current_patch is not None:
            ValidPatchStore.add_valid_patch(PatchStore.current_patch)
            successful_iterations += 1
        elif successful_test_execution and PatchStore.current_patch is None:
            successful_iterations += 1
        else:
            non_successful_iterations += 1

        # After every iteration the patch store clears his current patch and the Transformation Manager clears in all
        # transformation the holes which are stored.
        PatchStore.clear_current_patch()
        TransformationManager.clear_current_holes()

    # Set the value True, if the testsuite at least passes one time, false if it fails every single time. This is done
    # to check if there are passing testsuite sequences where no hole is reached.
    successful_sketch = successful_iterations > 0

    # Check if there are any valid patches in the patch store. If there were any executions the valid patch store's
    # patches are stored and cleared.
    valid_patches_found = ValidPatchStore.has_found_valid_patches()
    valid_patches = ValidPatchStore.valid_patch_list
    ValidPatchStore.clear_valid_patch_list()

    # If the testsuite is successful, and the valid patch store has patches they are written into a file.
    # If the testsuite is successful, and the valid patch store has nno patches they are ignored. The sketches are
    # useless, because the holes in the sketch aren't reached. If the testsuite is not successful and so as a
    # consequence there are no valid patches found (are only added if the testsuite is successful) then the sketch is
    # written as failing one.
    if successful_sketch and valid_patches_found:
        PatchWriter.print_and_write_passing_sketch(current_sketch_basename, valid_patches)
    elif successful_sketch and not valid_patches_found:
        PatchWriter.print_non_reaching_hole_sketch(current_sketch_basename)
    else:
        PatchWriter.print_failing_sketch(current_sketch_basename)


# Here the arguments of the user are fetched.
if __name__ == "__main__":
    if len(sys.argv) == 3:
        bug_file_input = str(sys.argv[1])
        unit_test_file_input = str(sys.argv[2])
        run_sketches(bug_file_input, unit_test_file_input)
    else:
        print("Please give arguments: bug file and unit testsuite suite")
