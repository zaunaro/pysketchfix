import os
from shutil import copyfile

from Stores.Hole import Hole
from Stores.PatchStore import PatchStore


def write_test_output(content, test_directory, test_basename):
    """
    Writes the test output of the TestRunner in the stores. Here the content is written in a file which is located
    in the same directory as the testsuite of the bug file.

    :param test_directory: The directory where the unit test for the bug file is located.
    :param test_basename: The name of the test for this bug file.
    :param content: The content which is written in the file.
    """
    file_name = os.path.join(test_directory, str(test_basename).replace(".py", "_") + "output.txt")
    file = open(file_name, "w+")
    file.write(content)
    file.close()


def parse_test_output(test_directory, test_basename):
    """
    This method is used in the old environment after executing the TestRunner. Therefore the FileHandler parses the
    output file which he has generated before in the TestRunner. Here the file is parsed for the hole content and
    this is added to the current PatchStore in this environment. Here also the failures of the test execution is listed.
    This is returned at the end, to identify if the test was successful or not.

    :param test_directory: The directory where the unit test for the bug file is located.
    :param test_basename: The name of the test for this bug file.
    :return: an Integer with the number of failures of the test.
    """
    # Open the output file and read the lines.
    file_name = os.path.join(test_directory, str(test_basename).replace(".py", "_") + "output.txt")
    file = open(file_name, "r")
    lines = file.readlines()
    file.close()
    # Save the variables which he has read currently.
    failures = ""
    hole_number = ""
    line_number = ""
    transformation_type = ""
    changed_code = ""
    varoperator = ""
    for line in lines:
        # If all variables are set then make a new hole and add it in the PatchStore. Then reset the information
        # for the next hole.
        if hole_number != "" and line_number != "" and transformation_type != "" and changed_code != "" \
                and varoperator != "":
            hole_new = Hole(int(hole_number), int(line_number), [changed_code], str(transformation_type),
                            str(varoperator))
            PatchStore.add_hole_to_patch(hole_new)
            hole_number = ""
            line_number = ""
            transformation_type = ""
            changed_code = ""
            varoperator = ""
        if line.__contains__("Failures:"):
            failures = line[line.index(":") + 1:]
        if line.__contains__("Hole:"):
            hole_number = line[line.index(":") + 1:]
        if line.__contains__("Type:"):
            transformation_type = line[line.index(":") + 1:]
        if line.__contains__("Line:"):
            line_number = line[line.index(":") + 1:]
        if line.__contains__("Varoperator:"):
            varoperator = line[line.index(":") + 1:]
        if line.__contains__("ChangedCode:"):
            array_str = line[line.index(":") + 1:]
            if array_str == "[]" or not array_str.__contains__("[") or not array_str.__contains__("]"):
                changed_code = ""
            else:
                array_str = array_str[array_str.index("[") + 1:array_str.index("]")]
                changed_code = array_str
    # Delete the test output file.
    os.remove(file_name)
    return int(failures)


def parse_file_for_content_as_string(file):
    """
    Parse the file and return the lines of it as String.

    :param file: The name of the file which is parsed.
    :return: a string with all lines of the file.
    """
    lines = ""
    bug_file = open(file)
    for line in bug_file.readlines():
        lines = lines + line
    bug_file.close()
    return lines


def get_lines_of_file(file):
    """
    Parse the file and return the number of lines.

    :param file: The name of the file which is parsed.
    :return: the number of lines in the file.
    """
    counter = 0
    bug_file = open(file)
    for _ in bug_file.readlines():
        counter += 1
    bug_file.close()
    return counter


def parse_file_for_content_as_array(file):
    """
    Parse the file and return the lines of it as an array.

    :param file: The name of the file which is parsed.
    :return: an array with all lines of the file.
    """
    lines = []
    bug_file = open(file)
    for line in bug_file.readlines():
        lines.append(line)
    bug_file.close()
    return lines


def copy_bug_file_to_backups(bug_file, backup_bug_file):
    """
    Copy the whole file in the backups folder.

    :param backup_bug_file: The backup folder where the bug file is currently stored.
    :param bug_file: The current bug_file
    """
    copyfile(bug_file, backup_bug_file)


def move_bug_file_from_backups(bug_file, backup_bug_file):
    """
    At the end of every execution the bug file will be copied back to the bug file and the backup file is removed.

    :param backup_bug_file: The backup folder where the bug file is currently stored.
    :param bug_file: The current bug file.
    """
    copyfile(backup_bug_file, bug_file)
    os.remove(backup_bug_file)


def change_bug_file_with_sketch(bug_file, sketch_file, sketch_directory):
    """
    Change the bug file with the sketch file in the sketch directory.

    :param sketch_file: The sketch file which is the replacement of the bug file.
    :param bug_file: The bug file which is replaced.
    :param sketch_directory: The directory of the sketches.
    """
    sketch_file = os.path.join(sketch_directory, sketch_file)
    copyfile(sketch_file, bug_file)


def write_patch_file(patch_basename, patch_content, patch_directory):
    """
    Take the patch basename and build the output file name. Make the file in the patches folder and add the content.

    :param patch_basename: The patch file which is created.
    :param patch_content: The content of the patch.
    :param patch_directory: The directory where the patches are located.
    """
    output_file = os.path.join(patch_directory, patch_basename)
    file = open(output_file, "w+")
    file.write(patch_content)
    file.close()
