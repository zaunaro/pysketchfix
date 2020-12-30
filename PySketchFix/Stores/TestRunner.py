import sys
import unittest

from Config import FileHandler
from Config.ConfigReader import ConfigReader
from Stores.PatchStore import PatchStore


def run(test_directory, test_basename, sketch_name):
    """
    This file is executed in a new python environment. This is done because the test loader execution can be not done
    in one environment. If you execute the code to run a unit test in the same environment again and again, the first
    sketch which is changed with the bug file is taken over and over again. So there could not be taken any further
    sketches later. So i tried to outsource it in a new environment where the file handler writes and output file. In
    there he puts in all patches which are created. Later this output file gets parsed in the old environment and
    this is done also by the next sketch and so on.
    You find the loader and the test discover code in this source:
    https://www.geeksforgeeks.org/python-logging-test-output-to-a-file/ Last Access: 02.12.2020
    If you want to have a more detailed information about this library then you can look at the documentary of the
    unit tests: https://docs.python.org/3/library/unittest.html Last Access: 02.12.2020

    :param test_directory: The directory where the unit test for the bug file is located.
    :param test_basename: The name of the test for this bug file.
    :param sketch_name: The sketch which is currently taken.
    """
    # Set the current sketch and test in the patch store.
    PatchStore.set_current_sketch_and_test(sketch_name, test_basename)
    # Get the verbosity of the test execution from the bug file.
    VERBOSITY = ConfigReader.get_verbosity()
    # Get the loader of the unit test and execute the unit test.
    loader = unittest.TestLoader()
    suite = loader.discover(test_directory, pattern=test_basename, top_level_dir=test_directory)
    runner = unittest.TextTestRunner(sys.stderr, verbosity=VERBOSITY).run(suite)
    # Get the failures of the unit test and write the content of each hole in the current patch of the PatchStore
    # in the output file.
    failures = len(runner.failures) + len(runner.errors)
    content = "Sketch:" + sketch_name + "\n"
    content += "Failures:" + str(failures) + "\n"
    if PatchStore.current_patch is not None:
        if len(PatchStore.current_patch.holes) != 0:
            for hole in PatchStore.current_patch.holes:
                content += hole.to_output_format() + "\n___\n"
    # Write the output in the file.
    FileHandler.write_test_output(content, test_directory, test_basename)


# Execute the TestRunner in a new environment therefore use the os.system method. Here give the following arguments
# to the script: The first argument is the test directory of the bug file, then the name of the bug file test and the
# last is the current sketch which is taken.
if __name__ == "__main__":
    input_test_directory = sys.argv[1]
    input_test_basename = sys.argv[2]
    input_sketch_name = sys.argv[3]
    run(input_test_directory, input_test_basename, input_sketch_name)
