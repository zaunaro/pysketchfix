# At first you have to make sure the package ast tokens is installed in your python directory
# Therefore: pip install asttokens from https://pypi.org/project/asttokens/, you need numphy and unittest as well.
# AT FIRST PLEASE SET UP THE CONFIGURATIONS FILE!

import PatchFinder
import SketchMaker

# Here you have to configure your Python Interpreter with which you want to run the process.
python_interpreter = "/Users/daniel/BachelorarbeitDZ/PySketchFix/venv/bin/python"

# The location where the sketch generator, ochiai and the patch finder are located.
sketch_generator = "/Users/daniel/BachelorarbeitDZ/PySketchFix/SketchMaker.py"
patch_finder = "/Users/daniel/BachelorarbeitDZ/PySketchFix/PatchFinder.py"

# Debuggers which are possible:
fault_localizer = "/Users/daniel/BachelorarbeitDZ/PySketchFix/FaultLocalizer.py"
OCHIAI = "ochiai"
TARANTULA = "tarantula"

# The buggy lines of the maximum bug file.
maximum_buggy_lines = "4,5"
maximum_bug_file = "/Users/daniel/BachelorarbeitDZ/PySketchFix/BugFile/maximum/maximum.py"
maximum_bug_file_test = "/Users/daniel/BachelorarbeitDZ/PySketchFix/BugFile/maximum/testsuite/test_maximum.py"
maximum_test_input = "/Users/daniel/BachelorarbeitDZ/PySketchFix/BugFile/maximum/tests_for_ochiai/input_tests.txt"
# buggy_lines = maximum_buggy_lines
# bug_file = maximum_bug_file
# bug_file_test = maximum_bug_file_test
# test_input = maximum_test_input

# The buggy lines of the minimum bug file.
minimum_buggy_lines = "4,5"
minimum_bug_file = "/Users/daniel/BachelorarbeitDZ/PySketchFix/BugFile/minimum/minimum.py"
minimum_bug_file_test = "/Users/daniel/BachelorarbeitDZ/PySketchFix/BugFile/minimum/testsuite/test_minimum.py"
minimum_test_input = "/Users/daniel/BachelorarbeitDZ/PySketchFix/BugFile/minimum/tests_for_ochiai/input_tests.txt"
# buggy_lines = minimum_buggy_lines
# bug_file = minimum_bug_file
# bug_file_test = minimum_bug_file_test
# test_input = minimum_test_input

# The buggy lines of the is prime bug file.
is_prime_buggy_lines = "6,5,3"
is_prime_bug_file = "/Users/daniel/BachelorarbeitDZ/PySketchFix/BugFile/is_prime/is_prime.py"
is_prime_bug_file_test = "/Users/daniel/BachelorarbeitDZ/PySketchFix/BugFile/is_prime/testsuite/test_is_prime.py"
is_prime_test_input = "/Users/daniel/BachelorarbeitDZ/PySketchFix/BugFile/is_prime/tests_for_ochiai/input_tests.txt"
buggy_lines = is_prime_buggy_lines
bug_file = is_prime_bug_file
bug_file_test = is_prime_bug_file_test
test_input = is_prime_test_input

# The buggy lines of the positive indicator function.
positive_indicator_buggy_lines = "2,3"
positive_indicator_bug_file = "/Users/daniel/BachelorarbeitDZ/PySketchFix/BugFile/positive_indicator/" \
                              "positive_indicator.py"
positive_indicator_bug_file_test = "/Users/daniel/BachelorarbeitDZ/PySketchFix/BugFile/positive_indicator/testsuite/" \
                                   "test_positive_indictator.py"
positive_indicator_test_input = "/Users/daniel/BachelorarbeitDZ/PySketchFix/BugFile/positive_indicator/tests_for_" \
                                "ochiai/input_tests.txt"
# buggy_lines = positive_indicator_buggy_lines
# bug_file = positive_indicator_bug_file
# bug_file_test = positive_indicator_bug_file_test
# test_input = positive_indicator_test_input

# The buggy lines of the mid bug file.
mid_buggy_lines = "6,2,1"
mid_bug_file = "/Users/daniel/BachelorarbeitDZ/PySketchFix/BugFile/mid/mid.py"
mid_bug_file_test = "/Users/daniel/BachelorarbeitDZ/PySketchFix/BugFile/mid/testsuite/test_mid.py"
mid_test_input = "/Users/daniel/BachelorarbeitDZ/PySketchFix/BugFile/mid/tests_for_ochiai/input_tests.txt"
# buggy_lines = mid_buggy_lines
# bug_file = mid_bug_file
# bug_file_test = mid_bug_file_test
# test_input = mid_test_input

# First run the fault localizer (Ochiai, Tarantula) to get the buggy lines (if you don't want to use your own).
# buggy_lines = FaultLocalizer.start_fault_localization(bug_file, test_input, OCHIAI)
# buggy_lines = FaultLocalizer.start_fault_localization(bug_file, test_input, TARANTULA)
# Run SketchFix
SketchMaker.generate_sketches(bug_file, buggy_lines)
PatchFinder.run_sketches(bug_file, bug_file_test)
# os.system(python_interpreter + " " + fault_localizer + " " + bug_file + " " + test_input + " " + TARANTULA)
# os.system(python_interpreter + " " + fault_localizer + " " + bug_file + " " + test_input + " " + OCHIAI)
# os.system(python_interpreter + " " + sketch_generator + " " + bug_file + " " + buggy_lines)
# os.system(python_interpreter + " " + sketch_runner + " " + bug_file + " " + bug_file_test)
