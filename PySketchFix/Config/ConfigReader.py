import configparser
import os
import re

from Config import FileHandler


class ConfigReader(object):
    """
    Holds the current bug file which will be sketched and then searched for a patch. Also here is the unit testsuite
    file, which tests_for_ochiai the current bug file. Also the project directory is hold here, to ensure that the right
    project folder is taken for the sketches and patches created. The information about transformation schemas (as a
    list) and the import statements of it are also hold here. The Config Reader can search fold config parameters in the
    config file.
    """
    BUG_FILE = ""
    UNIT_TEST_FILE = ""
    PROJECT_DIRECTORY = ""
    TRANSFORMATION_SCHEMAS = [['EXP'], ['COM'], ['LOG'], ['ARI'], ['EXP', 'LOG'], ['EXP', 'ARI'], ['EXP', 'COM'],
                              ['ARI', 'LOG'], ['ARI', 'COM'], ['LOG', 'COM'], ['EXP', 'ARI', 'LOG'],
                              ['EXP', 'ARI', 'COM'], ['EXP', 'LOG', 'COM'], ['ARI', 'LOG', 'COM'],
                              ['EXP', 'ARI', 'LOG', 'COM']]
    IMPORT_STATEMENTS = 'from Schemas.ComparisonTransformation import COMTransformation\n' \
                        'from Schemas.LogicalTransformation import LOGTransformation\n' \
                        'from Schemas.ArithmeticTransformation import ARITransformation\n' \
                        'from Schemas.ExpressionTransformation import EXPTransformation\n'
    TRANSFORMATIONS = ['COMTransformation', 'LOGTransformation', 'ARITransformation', 'EXPTransformation']
    SKETCHES_DIRECTORY = "BugFileSketches"
    BACKUP_DIRECTORY = "BugFileBackups"
    PATCHES_DIRECTORY = "BugFilePatches"
    CONFIG_FILE = "config.ini"
    UNIT_TEST_CONTENT = "import unittest"
    TESTRUNNER = "Stores/TestRunner.py"

    """
    Here also the information of coded debuggers and other configurations for the fault localization with ochiai is 
    located.
    """
    CODED_DEBUGGERS = ["tarantula", "ochiai"]

    @staticmethod
    def setup_environment_for_PatchFinder(bug_file, unit_test_file, project_directory):
        """
        Setup the project environment with the bug file which is changed and the unit testsuite file to it. As well as
        the project folder. Before the parameters are set, the input is checked for correctness.

        :param bug_file: The bug file.
        :param unit_test_file: The unit testsuite file.
        :param project_directory: The project directory of the project.
        :raise: RunTimeError, if the files are not python or the directory is not existent or the bug file is empty
        or contains transformations, or if the unit testsuite file is wrong or empty.
        """
        ConfigReader.setup_bug_file(bug_file)

        if not os.path.isfile(unit_test_file):
            raise RuntimeError("This is not a valid unit testsuite file: " + unit_test_file)
        if not bug_file.endswith('.py'):
            raise RuntimeError("The input unit testsuite file: " + unit_test_file + " is not Python.")
        if not ConfigReader.check_unit_test_file(unit_test_file):
            raise RuntimeError(
                "The input unit testsuite file:" + unit_test_file + " is empty or is not a unit testsuite.")
        else:
            ConfigReader.UNIT_TEST_FILE = unit_test_file

        if not os.path.exists(project_directory):
            raise RuntimeError("This is not a valid project directory: " + project_directory)
        else:
            ConfigReader.PROJECT_DIRECTORY = project_directory

    @staticmethod
    def setup_bug_file(bug_file):
        """
        Setup the project environment with the bug file which is changed.
        Before the parameters are set, the input is checked for correctness.

        :param bug_file: The bug file.
        :raise: RunTimeError, if the files are not python or the directory is not existent or the bug file is empty
        or contains transformations.
        """
        if not os.path.isfile(bug_file):
            raise RuntimeError("This is not a valid bug file: " + bug_file)
        if not bug_file.endswith('.py'):
            raise RuntimeError("The input bug file: " + bug_file + " is not Python.")
        if not ConfigReader.check_if_bug_file_is_sketch(bug_file):
            raise RuntimeError("The input bug file: " + bug_file + " is empty or contains transformation schemas.")
        else:
            ConfigReader.BUG_FILE = bug_file

    @staticmethod
    def setup_environment_for_SketchMaker(bug_file, project_directory):
        """
        Setup the project environment with the bug file which is changed and the project folder.
        Before the parameters are set, the input is checked for correctness.

        :param bug_file: The bug file.
        :param project_directory: The project directory of the project.
        :raise: RunTimeError, if the files are not python or the directory is not existent or the bug file is empty
        or contains transformations.
        """
        ConfigReader.setup_bug_file(bug_file)

        if not os.path.exists(project_directory):
            raise RuntimeError("This is not a valid project directory: " + project_directory)
        else:
            ConfigReader.PROJECT_DIRECTORY = project_directory

    @staticmethod
    def check_unit_test_file(unit_test_file):
        """
        Check if the unit testsuite file is a unit testsuite file, contains tests_for_ochiai and is not empty.

        :param unit_test_file: The unit testsuite file which is checked.
        :return: True, if the unit testsuite file is valid, false otherwise.
        """
        test_file_lines = FileHandler.parse_file_for_content_as_string(unit_test_file)
        return re.search(ConfigReader.UNIT_TEST_FILE, test_file_lines)

    @staticmethod
    def check_if_bug_file_is_sketch(bug_file):
        """
        Here the bug file is checked weather the content of it contains a transformation or is empty. So the bug file is
        a sketch and the original content could not be written back by the last execution.

        :param bug_file: The bug file which is checked.
        :return: True, if no transformation is in it, false otherwise.
        """
        bug_file_lines = FileHandler.parse_file_for_content_as_string(bug_file)
        for transformation in ConfigReader.TRANSFORMATIONS:
            if re.search(transformation, bug_file_lines):
                return False
        return True

    @staticmethod
    def get(section, key):
        """
        Gets a value by key and section from the config file.

        :param section: The section where the key is searched.
        :param key: The key which is searched.
        :return: The value of the key.
        :raise: RunTimeError: if the file does not exist.
        """
        config_file = os.path.join(os.path.dirname(__file__), ConfigReader.CONFIG_FILE)
        if not os.path.isfile(config_file):
            raise RuntimeError("This is not a valid config file: " + config_file)
        config = configparser.ConfigParser()
        config.read(config_file)
        return config.get(section, key)

    @staticmethod
    def get_fom_performance_configurations(key):
        """
        :param key: The key in the performance configuration which is searched.
        :return: the value of the key in the performance configurations.
        """
        value = ConfigReader.get("PerformanceConfigurations", key)
        return value

    @staticmethod
    def get_strict_patch_treatment():
        """
        :return: True, if a patch is only correct if the whole testsuite suite passes, false if the sketch is correct,
        if the original number of failing testsuite cases is now lower or equal.
        :raise RuntimeError: if the value of the print patches for each sketch is not true or false.
        """
        value = ConfigReader.get_fom_performance_configurations("STRICT_PATCH_TREATMENT")
        if value == "True":
            return True
        elif value == "False":
            return False
        else:
            raise RuntimeError("The config parameter for strict patch treatment is not set to bool.")

    @staticmethod
    def get_print_for_every_sketch_parameter():
        """
        :return: True, if for every sketch an output file with its patches should be created, false otherwise.
        :raise RuntimeError: if the value of the print patches for each sketch is not true or false.
        """
        value = ConfigReader.get_fom_performance_configurations("PRINT_PATCHES_FOR_EACH_SKETCH")
        if value == "True":
            return True
        elif value == "False":
            return False
        else:
            raise RuntimeError("The config parameter for print patches for each sketch is not set to bool.")

    @staticmethod
    def get_debug_mode():
        """
        :return: True, if the debug mode is on and more output is generated.
        :raise RuntimeError: if the value of the debug mode is not true or false.
        """
        value = ConfigReader.get_fom_performance_configurations("DEBUG")
        if value == "True":
            return True
        elif value == "False":
            return False
        else:
            raise RuntimeError("The config parameter for debug is not set to bool.")

    @staticmethod
    def get_max_iterations():
        """
        :return: the maximal iterations done in one execution of a testsuite.
        :raise RuntimeError if the value is less or equal then 0, then no iteration is done.
        """
        value = int(ConfigReader.get_fom_performance_configurations("MAX_ITERATIONS"))
        if value <= 0:
            raise RuntimeError("The config parameter for max iterations is less or equal 0.")
        return value

    @staticmethod
    def get_considered_lines_variables():
        """
        :return: the array of all considered lines of the closer variables for the expression transformations.
        :raise RuntimeError if the value is less then 0, then no considered lines could be done.
        """
        value = int(ConfigReader.get_fom_performance_configurations("MAX_CONSIDERED_LINES_VARIABLES"))
        if value < 0:
            raise RuntimeError("The config parameter for considered lines for closer variables is less then 0.")
        return list(range(0, value))

    @staticmethod
    def get_verbosity():
        """
        Gets the verbosity of the bug files with which the unit testsuite could be run.
        """
        return int(ConfigReader.get_fom_performance_configurations("TEST_VERBOSITY"))

    @staticmethod
    def get_depth():
        """
        :return: the array with depth how deep the tree of statements is parsed for a transformation.
        :raise RuntimeError if the value is less then 1, then no transformation is done.
        """
        value = int(ConfigReader.get_fom_performance_configurations("MAX_DEPTH"))
        if value < 1:
            raise RuntimeError("The config parameter for depth of transformation is less then 1.")
        return list(range(1, value))

    @staticmethod
    def get_transformation_schema_combinations():
        """
        :return: all possible combinations of transformations which are done to find a patch.
        """
        return ConfigReader.TRANSFORMATION_SCHEMAS

    @staticmethod
    def get_import_statements():
        """
        :return: the import statements which are inserted in the bug file to ensure the transformations are found.
        """
        return ConfigReader.IMPORT_STATEMENTS

    @staticmethod
    def get_sketch_directory():
        """
        :return: the directory where the created sketches are located.
        :raise: RunTimeError, if the directory does not exist.
        """
        sketch_directory = os.path.join(ConfigReader.PROJECT_DIRECTORY, ConfigReader.SKETCHES_DIRECTORY)
        if not os.path.exists(sketch_directory):
            raise RuntimeError("This is not a valid sketch directory: " + sketch_directory)
        return sketch_directory

    @staticmethod
    def get_patch_directory():
        """
        :return: the directory where the created patches are located.
        :raise: RunTimeError, if the directory does not exist.
        """
        patches_directory = os.path.join(ConfigReader.PROJECT_DIRECTORY, ConfigReader.PATCHES_DIRECTORY)
        if not os.path.exists(patches_directory):
            raise RuntimeError("This is not a valid patches directory: " + patches_directory)
        return patches_directory

    @staticmethod
    def get_unit_test_file():
        """
        :return: the unit testsuite file of the bug file.
        """
        return ConfigReader.UNIT_TEST_FILE

    @staticmethod
    def get_unit_test_file_basename():
        """
        :return: the base name of the unit testsuite file. This is the name with the '.py' annotation at the end.
        """
        return os.path.basename(ConfigReader.UNIT_TEST_FILE)

    @staticmethod
    def get_unit_test_file_directory():
        """
        :return: the unit testsuite file's directory.
        """
        unit_test_file = ConfigReader.get_unit_test_file()
        unit_test_file_basename = ConfigReader.get_unit_test_file_basename()
        return unit_test_file.replace(unit_test_file_basename, "")

    @staticmethod
    def get_bug_file():
        """
        :return: the bug file with the path and the annotation.
        """
        return ConfigReader.BUG_FILE

    @staticmethod
    def get_backup_bug_file():
        """
        :return: the Backup file (with path and type) for the bug file to ensure it is not deleted.
        :raise: RunTimeError, if the directory does not exist.
        """
        backup_bug_file_directory = os.path.join(ConfigReader.PROJECT_DIRECTORY, ConfigReader.BACKUP_DIRECTORY)
        if not os.path.exists(backup_bug_file_directory):
            raise RuntimeError("This is not a valid backup directory: " + backup_bug_file_directory)
        backup_bug_file = os.path.join(backup_bug_file_directory, ConfigReader.get_bug_file_basename())
        return backup_bug_file

    @staticmethod
    def get_bug_file_basename():
        """
        :return: the base name of the bug file. This is the name with the '.py' annotation at the end.
        """
        bug_file = ConfigReader.get_bug_file()
        return os.path.basename(bug_file)

    @staticmethod
    def get_bug_file_name():
        """
        :return: the blank name of the bug file. This is the name without the '.py' annotation at the end.
        """
        bug_file_basename = ConfigReader.get_bug_file_basename()
        return bug_file_basename.replace(".py", "")

    @staticmethod
    def get_coded_debuggers():
        """
        :return: the array of coded debuggers which are possible for fault localization.
        """
        return ConfigReader.CODED_DEBUGGERS

    @staticmethod
    def get_number_of_considered_lines_fault_localization():
        """
        :return: the number of lines which should be returned in the fault localization. So here for example the top 10
        lines could be returned of a file where a bug is possible located.
        """
        value = ConfigReader.get("FaultLocalizingConfigurations", "CONSIDERED_LINES_FAULT_LOCALIZATION")
        return int(value)

    @staticmethod
    def get_python_coverage():
        """
        :return: the python interpreter where the coverage library is located.
        """
        value = ConfigReader.get("FaultLocalizingConfigurations", "PYTHON_COVERAGE")
        return str(value)

    @staticmethod
    def get_test_runner():
        """
        :return: the TestRunner.py script in the Stores directory.
        """
        return os.path.join(ConfigReader.PROJECT_DIRECTORY, ConfigReader.TESTRUNNER)

    @staticmethod
    def get_python_interpreter():
        """
        :return: the current interpreter which is configured in the python file.
        """
        value = ConfigReader.get("FaultLocalizingConfigurations", "PYTHON_INTERPRETER")
        return str(value)
