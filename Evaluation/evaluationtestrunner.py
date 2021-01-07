import sys
import unittest


def run(test_directory, test_basename, result_file):
    """
    This file is executed in a new python environment. This is done because the test loader execution can be not done
    in one environment. If you execute the code to run a unit test in the same environment again and again. So as a
    consequence you get the same results for every new iteration.
    You find the loader and the test discover code in this source:
    https://www.geeksforgeeks.org/python-logging-test-output-to-a-file/ Last Access: 02.12.2020
    If you want to have a more detailed information about this library then you can look at the documentary of the
    unit tests: https://docs.python.org/3/library/unittest.html Last Access: 02.12.2020

    :param test_directory: The directory where the unit test for the bug file is located.
    :param test_basename: The name of the test for this bug file.
    :param result_file: The file where the result is stored.
    """
    VERBOSITY = 2
    loader = unittest.TestLoader()
    suite = loader.discover(test_directory, pattern=test_basename, top_level_dir=test_directory)
    runner = unittest.TextTestRunner(sys.stderr, verbosity=VERBOSITY).run(suite)
    # Get the failures of the unit test and write the number of failures to the output file.
    content = "failures=" + str(len(runner.failures)) + "\n"
    content += "errors=" + str(len(runner.errors))
    file = open(result_file, "w+")
    file.write(content)
    file.close()


# Execute the TestRunner in a new environment therefore use the os.system method. Here give the following arguments
# to the script: The first argument is the test directory of the bug file, then the name of the bug file test and the
# last is the file which is created.
if __name__ == "__main__":
    input_test_directory = sys.argv[1]
    input_test_basename = sys.argv[2]
    input_result_file = sys.argv[3]
    run(input_test_directory, input_test_basename, input_result_file)
