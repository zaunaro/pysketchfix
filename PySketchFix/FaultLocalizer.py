import math
import os
import sys
import unittest
from subprocess import check_output

from Config import FileHandler
from Config.ConfigReader import ConfigReader


def start_fault_localization(bug_file, input_file, DEBUGGER):
    """
    Start the fault localization which returns an array of buggy lines (from highest suspicious to lowest) where
    the bug in the file could be located.

    :param bug_file: The bug file which is tested.
    :param input_file: A .txt file which stores all tests at least more then 1 for coverage.
    :param DEBUGGER: The debugger Ochiai or Tarantula which is used.
    :raise RuntimeError: if the debugger is not in the array of possible debuggers (Tarantula, Ochiai).
    """
    # The debugger: Can only be "tarantula", "ochiai" so it is checked if the input debugger is in the array.
    if DEBUGGER not in ConfigReader.get_coded_debuggers():
        raise RuntimeError("The debugger: " + DEBUGGER + " is not coded yet.")
    # Check the bug file if it is valid and set it in the config reader.
    ConfigReader.setup_bug_file(bug_file)
    # Check the input file and the testsuite files if they are valid.
    test_files = open_input_file(input_file)
    # Get the number of lines in the bug file.
    lines_of_code = FileHandler.get_lines_of_file(bug_file)
    # Number of total failing tests.
    number_of_total_failing_tests = 0
    # Number of total passing tests.
    number_of_total_passing_tests = 0
    # The lines array contains objects of code lines. They are generated here for every line.
    code_lines = []
    for line_number in range(1, lines_of_code + 1):
        code_line = CodeLine(line_number, DEBUGGER)
        code_lines.append(code_line)

    # Now for every file in the test files the tests are executed and the number of passing and failing tests
    # changed.
    for test_file in test_files:
        test_name = os.path.basename(test_file)
        test_directory = test_file.replace(test_name, "")
        print("-------------------------------------------------------------------------------------------------------")
        print(test_name)
        print("-------------------------------------------------------------------------------------------------------")

        # If the tests fails the total number of failing or passing tests is incremented.
        failing_test = is_failing_test(test_name, test_directory)
        if failing_test:
            number_of_total_failing_tests += 1
        else:
            number_of_total_passing_tests += 1

        # Now the covered lines of the tests are fetched. Therefore the coverage is created. Then for all lines
        # which the test covers the corresponding code line number of failing tests (if the test fails) or the number of
        # passing tests (if the test fails) is incremented.
        covered_lines = get_covered_lines(bug_file, test_file)
        for covered_line in covered_lines:
            if failing_test:
                code_lines[covered_line - 1].increment_number_of_failing_tests()
            else:
                code_lines[covered_line - 1].increment_number_of_passing_tests()

    # For every line in the code lines the suspicious value is calculated with the total number of failing and passing
    # tests. (If everything is done.)
    for code_line in code_lines:
        code_line.calculate_sus_value(number_of_total_failing_tests, number_of_total_passing_tests)

    # Then the code lines are sorted with the sus value.
    sorted_code_lines = sort_code_lines(code_lines)

    # Now the output is generated.
    print("-------------------------------------------------------------------------------------------------------")
    print("Suspicious:")
    array_output = ""
    output = ""
    counter = 0
    number_of_considered_lines = ConfigReader.get_number_of_considered_lines_fault_localization()
    print("Line\t\t|\t\t" + "Ochiai\t\t|\t\tTarantula\t\t")
    for sorted_code_line in sorted_code_lines:
        counter += 1
        output += (str(sorted_code_line.line_number) + ": " + str(sorted_code_line.suspicious_value)) + "\t\t|\t\t"
        output += str(sorted_code_line.ochiai_value) + "\t\t|\t\t" + str(sorted_code_line.tarantula_value) + "\n"
        array_output += str(sorted_code_line.line_number) + ","
        if counter == number_of_considered_lines:
            break
    array_output = array_output[0:len(array_output) - 1]
    print(output)
    print("-------------------------------------------------------------------------------------------------------")
    print("Buggy Lines for PySketchFix taken debugger: " + DEBUGGER)
    return array_output


def sort_code_lines(code_lines):
    """
    The code lines contain code lines of the bug file. The task of this method is to sort this list by the highest
    suspicious value of the code line.

    :param code_lines: the list of code lines.
    :return: the sorted code lines from highest suspicious to lowest.
    """
    sorted_code_lines = []
    while len(code_lines) != 0:
        # Get the line where the highest suspicious value is in the current code_lines array.
        line_number = get_highest_sus_value(code_lines)
        new_code_lines = []
        # Make a new code lines array where you delete the line number.
        for code_line in code_lines:
            if code_line.line_number != line_number:
                new_code_lines.append(code_line)
            if code_line.line_number == line_number:
                sorted_code_lines.append(code_line)
        # Set the new code lines array.
        code_lines = new_code_lines
    return sorted_code_lines


def get_highest_sus_value(code_lines):
    """
    Return the highest suspicious line in the code lines array.

    :param code_lines: The code lines of the bug file. This changes with every iteration (the current highest is
    deleted) until the array is empty.
    :return: the line where the highest suspicious value is.
    """
    # Set the current highest sus value to the lowest number to have an initial value of the current highest sus value.
    current_highest_sus_value = -1000000
    current_line_number = 0
    for code_line in code_lines:
        # Check for every line in the array if the current highest sus value is bigger then the current highest sus
        # value. If it is higher then this is the new current line number.
        if current_highest_sus_value < code_line.suspicious_value:
            current_highest_sus_value = code_line.suspicious_value
            current_line_number = code_line.line_number
    return current_line_number


def is_failing_test(test_name, test_directory):
    """
    Check if the test is failing.
    You find the loader and the test discover code in this source:
    https://www.geeksforgeeks.org/python-logging-test-output-to-a-file/ Last Access: 02.12.2020
    If you want to have a more detailed information about this library then you can look at the documentary of the
    unit tests: https://docs.python.org/3/library/unittest.html Last Access: 02.12.2020

    :param test_name: The test which is executed.
    :param test_directory: The directory where the test is located.
    :return: True, if the test fails, False otherwise.
    """
    # Get the verbosity of test execution from the config value.
    verbosity = ConfigReader.get_verbosity()
    # Here the tests are run and the number of failing or error tests are counted.
    loader = unittest.TestLoader()
    suite = loader.discover(test_directory, pattern=test_name)
    runner = unittest.TextTestRunner(sys.stderr, verbosity=verbosity).run(suite)
    # The number of failing tests is the length of the array of failures and errors.
    number_of_failing_tests = 0
    if runner.failures is not None:
        number_of_failing_tests += len(runner.failures)
    if runner.errors is not None:
        number_of_failing_tests += len(runner.errors)
    number_of_passing_tests = suite.countTestCases() - number_of_failing_tests
    print("-------------------------------------------------------------------------------------------------------")
    print("Test Execution:")
    print("Failing: " + str(number_of_failing_tests) + "\nPassing: " + str(number_of_passing_tests))
    return number_of_failing_tests == 0


def get_covered_lines(bug_file, test_file):
    # TODO Coverage funktioniert noch nicht.
    # Get the coverage library from the config value.
    PYTHON_INTERPRETER = ConfigReader.get_python_coverage()
    # TODO Quellen zur Auswertung von Coverage Report?.
    # VON https://github.com/EririSawamura/Debugging-tools-for-cpp-python
    # https://stackoverflow.com/questions/47497001/python-unit-test-coverage-for-multiple-modules
    result = os.popen(PYTHON_INTERPRETER + " run " + test_file)
    res = result.read()
    for line in res.splitlines():
        pass
    Report = check_output(PYTHON_INTERPRETER + " report -m " + test_file, shell=True).decode()
    ReportList = Report.split("\n")
    ReportInfo = ReportList[2].split(" ")
    ReportInfo = [x.replace('\r', '') for x in ReportInfo if x != '']
    ReportInfo = [x.replace(',', '') for x in ReportInfo]
    TotalLength = int(ReportInfo[1])
    MissingLine = []
    CoverLine = []
    if len(ReportInfo) > 4:
        for i in range(4, len(ReportInfo)):
            if '-' in ReportInfo[i]:
                RInfoList = ReportInfo[i].split('-')
                L = RInfoList[0]
                R = RInfoList[1]
                for i in range(int(L), int(R) + 1):
                    MissingLine.append(i)
            else:
                MissingLine.append(int(ReportInfo[i]))
    for i in range(1, TotalLength + 1):
        if i not in MissingLine:
            CoverLine.append(i)
    os.remove(".coverage")
    print("-------------------------------------------------------------------------------------------------------")
    print("Coverage:")
    print(Report)
    print(MissingLine)
    print(CoverLine)
    return CoverLine


def open_input_file(input_tests):
    """
    Get a path to a input file where paths to different tests are written. These get extracted and returned as an array.
    Before this all is done, the file is checked if it is valid. Here also the files are checked if they are unit tests.

    :param input_tests: The file where the tests are written into.
    :return: a string array where the paths to the tests are written.
    :raise: RuntimeError, if the file does not exists is not a txt file, is empty or has only one testsuite in it.
    Here also a RuntimeError is raised, if the test file input is not valid or does not exist.
    """
    if not os.path.isfile(input_tests):
        raise RuntimeError("This is not a valid input file: " + input_tests)
    if not input_tests.endswith('.txt'):
        raise RuntimeError("The input file: " + input_tests + " is not Txt.")
    array_of_tests = []
    input_file = open(input_tests)
    for test in input_file.readlines():
        test = test.replace("\n", "")
        if not os.path.isfile(test):
            raise RuntimeError("This is not a input test file: " + test)
        if not test.endswith('.py'):
            raise RuntimeError("This is not a input test file which is Python: " + test)
        array_of_tests.append(test)
    input_file.close()
    if len(array_of_tests) == 1:
        raise RuntimeError("The input file: " + input_tests + " has only one test, please make at least two tests.")
    if len(array_of_tests) == 0:
        raise RuntimeError("The input file: " + input_tests + " is empty.")
    return array_of_tests


class CodeLine(object):
    """
    A Code line object stores the line number and the suspicious value of it.
    """

    def __init__(self, line_number, DEBUGGER):
        """
        :param line_number: The line number in the bug file.
        :param DEBUGGER: The debugger which is used for the suspicious value.
        """
        self.line_number = line_number
        self.DEBUGGER = DEBUGGER
        # Count the number of failing tests and passing tests.
        self.number_of_failing_tests = 0
        self.number_of_passing_tests = 0
        # The suspicious value with the coded debuggers value (ochiai or tarantula)
        self.suspicious_value = 0
        self.ochiai_value = 0
        self.tarantula_value = 0

    def increment_number_of_failing_tests(self):
        """
        Increments the number of failing tests. This is only incremented if a test covers this line. And if the test
        is failing at all then this number is incremented.
        """
        self.number_of_failing_tests += 1

    def increment_number_of_passing_tests(self):
        """
        Increments the number of passing tests. This is only incremented if a test covers this line. And if the test
        is passing at all then this number is incremented.
        """
        self.number_of_passing_tests += 1

    def calculate_sus_value(self, number_of_total_failing_tests, number_of_total_passing_tests):
        """
        Calculates the suspicious value of all coded debuggers.

        :param number_of_total_failing_tests: The number of total failing tests.
        :param number_of_total_passing_tests: The number of total passing tests.
        """
        self.calculate_ochiai(number_of_total_failing_tests)
        self.calculate_tarantula(number_of_total_failing_tests, number_of_total_passing_tests)
        # The suspicious value (with which it sorted later) is the debugger which is taken as input.
        if self.DEBUGGER == 'ochiai':
            self.suspicious_value = self.ochiai_value
        elif self.DEBUGGER == 'tranatula':
            self.suspicious_value = self.tarantula_value

    def calculate_ochiai(self, number_of_total_failing_tests):
        """
        Calculate the ochiai suspicious value. The calculation is taken by the following paper:
        Evaluating and Improving Fault Localization - Gordon Fraser Last Access: 29.12.2020

        :param number_of_total_failing_tests: The number of total failing tests.
        """
        sqrt = math.sqrt(number_of_total_failing_tests * (self.number_of_failing_tests + self.number_of_passing_tests))
        if sqrt == 0:
            self.ochiai_value = 0
        else:
            self.ochiai_value = round(self.number_of_failing_tests / sqrt, 2)

    def calculate_tarantula(self, number_of_total_failing_tests, number_of_total_passing_tests):
        """
        Calculate the tarantula suspicious value. The calculation is taken by the following paper:
        Evaluating and Improving Fault Localization - Gordon Fraser Last Access: 29.12.2020

        :param number_of_total_failing_tests: The number of total failing tests.
        :param number_of_total_passing_tests: The number of total passing tests.
        """
        if number_of_total_failing_tests == 0 or number_of_total_passing_tests == 0:
            self.tarantula_value = 0
        else:
            dividend = self.number_of_failing_tests / number_of_total_failing_tests + \
                       self.number_of_passing_tests / number_of_total_passing_tests
            if dividend == 0:
                self.tarantula_value = 0
            else:
                self.tarantula_value = round((self.number_of_failing_tests / number_of_total_failing_tests) / dividend,
                                             2)


# Here the arguments of the user are fetched.
if __name__ == "__main__":
    if len(sys.argv) == 4:
        bug_file_input_SYS = str(sys.argv[1])
        input_file_SYS = str(sys.argv[2])
        DEBUGGER_SYS = str(sys.argv[3])
        arr = start_fault_localization(bug_file_input_SYS, input_file_SYS, DEBUGGER_SYS)
        print(arr)
    else:
        print(
            "Please give arguments: bug file and a path to a txt file where the tests are listed and the debugger you "
            "would like to use.")
