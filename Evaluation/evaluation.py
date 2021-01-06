import os
import sys
import unittest

import PatchFinder
import SketchMaker


def main():
    """
    Here PySketchFix is evaluated! To ensure Evaluating PySketchFix right, Ochiai and Tarantula are not tested. (
    where the bug is identified). The buggy lines (-) where given. This isn't even possible because there is only
    one test suite given.
    """

    PROJECTS_FOLDER = "/Users/daniel/Bachelorarbeit/Projects"
    """
    Define the folder where the github projects to evaluate were cloned to. If you don't have cloned the Projects
    don't worry the script does this by itself, if they aren't cloned yet.
    """

    BUGS_IN_PY_FOLDER = '/Users/daniel/Bachelorarbeit/bugsinpy'
    """
    Define the folder where the BugsInPy Folder is cloned to. Here it is important to clone the project by yourself:
    https://github.com/soarsmu/BugsInPy.
    """

    START_PY_FIX_WITH_PASSING_TEST = True
    """
    If this value is true, then also bugs which have a passing test suite are started to generate sketches. They are
    useless because SketchFix thinks that every sketch is a patch because all tests are passing. But for evaluation 
    reasons, to identify the number of possible created sketches I decided to add this function.
    """

    GENERATE_RESULT = False
    """
    If this value is true, then an output file is generated.
    """

    GENERATE = False
    """
    If this value is true, then only generations are started and no testing for the generated sketches. If the value is 
    false and also the generate and test value is false then only the test of the projects are run.
    """

    GENERATE_AND_TEST = True
    """
    If this value is true, then generations are started and also testing for the generated sketches. If the value is 
    false and also the generate value is false then only the test of the projects are run. Test only be run if it is a 
    unit test runner.
    """

    FOLDER_FOR_RESULTS = "/Users/daniel/Bachelorarbeit/pysketchfix/Evaluation/Results"
    """
    Define the folder, where the output of the test execution should be stored.
    """

    VERBOSITY = 2
    """
    Set the verbosity of the test execution
    """

    MAXIMUM_BUG_LINES = 5
    """
    Defines the top suspicious lines which are taken to generate sketches. If you would like to add more suspicious 
    lines then feel free, but the runtime will be very slow.
    """

    PROJECTS_TO_EVALUATE = ['youtube-dl']
    """
    Define the names of the projects which should be evaluated with bugs in py.
    """

    for project_to_evaluate in PROJECTS_TO_EVALUATE:
        # All bugs where the failing tests are stored. A failing test is a test which has a failure or an error.
        failing_tests_array = []
        # All bugs where passing tests are stored.
        passing_tests_array = []
        # All bugs where the bug.info or no bug.patch file is not found or empty.
        no_info_or_patch_file_array = []
        # All bugs where the suspicious lines are empty.
        empty_suspicious_lines_array = []

        # Open the path where the output file is stored and set it as output for prints.
        if GENERATE_RESULT:
            sys.stdout = open(os.path.join(FOLDER_FOR_RESULTS, project_to_evaluate + ".txt"), 'w+')
        print()
        print("#######################################################################################################")
        print("                             PROJECT: " + project_to_evaluate)
        print("#######################################################################################################")
        # Current folder in bugsInPy of the project:
        project_bugs_in_py_folder = os.path.join(BUGS_IN_PY_FOLDER, 'projects', project_to_evaluate)

        # First of all get the project info in the project folder of bugs in py project.
        project_info = os.path.join(project_bugs_in_py_folder, 'project.info')
        if not os.path.exists(project_info):
            print("FAIL! The project info: " + str(project_info) + " in the project " + str(project_to_evaluate) +
                  " does not exists. Next project is taken")
            continue

        # Clone the repository in the projects folder if it doesn't exists already. Therefore get the github url from
        # the project info and make a new folder in the projects.
        github_url = open_info_for_github_url(project_info)
        github_repo_folder = os.path.join(PROJECTS_FOLDER, project_to_evaluate)
        cloned = clone_git_repo(github_url, github_repo_folder)
        if not cloned:
            print("FAIL! The project :" + str(project_to_evaluate) + " could not be cloned. Next project is taken")
            continue

        # Get the folder where all the bugs are located in the bugs in py directory.
        bugs_folder_in_bugs_in_py_folder = os.path.join(project_bugs_in_py_folder, 'bugs')
        if not os.path.exists(bugs_folder_in_bugs_in_py_folder):
            print("The bugs folder: " + str(bugs_folder_in_bugs_in_py_folder) + " to the project " +
                  str(project_to_evaluate) + " does not exists. Next project is taken")
            continue

        # List all bug folders in the directory and add it to an array if they are numeric.
        folders = os.listdir(bugs_folder_in_bugs_in_py_folder)
        folder_numbers = []
        for folder in folders:
            if str.isnumeric(str(folder)):
                folder_numbers.append(int(str(folder)))
        folder_numbers.sort()

        # Then get the buggy lines to the bugs which are located in the bugs in py directory.
        print(".......................................................................................................")
        print("BUGGY LINES:")
        buggy_lines = get_buggy_lines(folder_numbers, bugs_folder_in_bugs_in_py_folder, MAXIMUM_BUG_LINES)
        print(".......................................................................................................")

        for folder_number in folder_numbers:
            # Then get to the folder where the current bug is located.
            current_bug_folder = os.path.join(str(bugs_folder_in_bugs_in_py_folder), str(folder_number))

            # At first the bug number is stored and printed.
            bug_number = str(folder_number)
            print()
            print("+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+")
            print()
            print("                                          BUG: " + str(bug_number))
            print()
            print("+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+")

            # Then get the buggy lines to the bug file.
            bug_number_int = int(bug_number)
            buggy_line = buggy_lines[bug_number_int - 1]
            if len(buggy_line) == 0:
                print("x FAIL! Suspicious lines are empty!")
                empty_suspicious_lines_array.append(bug_number_int)
                continue

            # Get the bug info file in the current bug folder. Continue if it is empty or does not exist.
            bug_info_file = os.path.join(current_bug_folder, 'bug.info')
            if not bug_information_file_is_valid(bug_info_file):
                print("x FAIL! The Bug Info file: " + str(bug_info_file) + " to the project " + str(
                    project_to_evaluate) + " with bug: " + str(bug_number) + "does not exists. Next bug is taken")
                no_info_or_patch_file_array.append(bug_number_int)
                continue

            # Get the bug patch file in the current bug folder. Continue if it is empty or does not exist.
            bug_patch_file = os.path.join(current_bug_folder, 'bug_patch.txt')
            if not bug_information_file_is_valid(bug_patch_file):
                print("x FAIL! The Bug Patch file: " + str(bug_info_file) + " to the project " + str(
                    project_to_evaluate) + " with bug: " + str(bug_number) + "does not exists. Next bug is taken")
                no_info_or_patch_file_array.append(bug_number_int)
                continue

            # Then open the bug information to store the buggy commit id.
            buggy_commit_id = open_info_for_buggy_commit_id(bug_info_file)
            if buggy_commit_id == "":
                print("x FAIL! The buggy commit id in bug: " + str(bug_number) + " to the project " + str(
                    project_to_evaluate) + " does not exists. Next bug is taken")
                no_info_or_patch_file_array.append(bug_number_int)
                continue

            # Reset the git hub repo to the buggy commit id.
            print("GIT RESET TO: " + buggy_commit_id)
            reset_git_repo_to_buggy_commit(github_repo_folder, buggy_commit_id)

            # Then the bug test file is fetched with the bug info file. Then join the github repo folder with the
            # bug test file.
            bug_test_file = open_info_for_bug_test_file(bug_info_file)
            bug_test_file = os.path.join(github_repo_folder, bug_test_file)
            if not os.path.isfile(bug_test_file):
                print("x FAIL! The TEST file: " + str(bug_test_file) + " to the project " + str(project_to_evaluate) +
                      " with bug: " + str(bug_number) + "does not exists. Next bug is taken")
                no_info_or_patch_file_array.append(bug_number_int)
                continue

            # Then the bug file itself is fetched with the patch file. Then join the github repo folder with the
            # bug file.
            bug_file = open_patch_for_bug_file(bug_patch_file)
            bug_file = os.path.join(github_repo_folder, bug_file)
            if not os.path.isfile(bug_file):
                print("x FAIL! The BUG file: " + str(bug_file) + " to the project " + str(project_to_evaluate) +
                      " with bug: " + str(bug_number) + "does not exists. Next bug is taken")
                no_info_or_patch_file_array.append(bug_number_int)
                continue

            # Increment the number of evaluated bugs if everything is setup well.
            print("bug_file = " + str(bug_file))
            print("bug_test_file = " + str(bug_test_file))

            # Now the test file is run to get to know, if the test passes or not.
            print("TEST EXECUTION:")
            loader = unittest.TestLoader()
            UNIT_TEST_FILE_BASENAME = os.path.basename(bug_test_file)
            UNIT_TEST_FILE_DIRECTORY = bug_test_file.replace(UNIT_TEST_FILE_BASENAME, "")
            suite = loader.discover(UNIT_TEST_FILE_DIRECTORY, pattern=UNIT_TEST_FILE_BASENAME)
            runner = unittest.TextTestRunner(sys.stderr, verbosity=VERBOSITY).run(suite)

            # If there are no errors then the bug is added to the array of passing test cases.
            if len(runner.failures) + len(runner.errors) == 0:
                print("✓ SUCCESSFUL! TEST PASSES")
                passing_tests_array.append(bug_number_int)
                if not START_PY_FIX_WITH_PASSING_TEST:
                    print("x PySketchFix could not be started if test passes...")
                else:
                    # If the generate flag is set, then also for passing tests sketches are generated.
                    if GENERATE:
                        print("✓ PySketchFix is started...")
                        SketchMaker.generate_sketches(bug_file, buggy_line)
            else:
                print("x FAIL! Test fails or has errors.")
                failing_tests_array.append(bug_number_int)
                if GENERATE:
                    print("✓ PySketchFix is started...")
                    SketchMaker.generate_sketches(bug_file, buggy_line)
                elif GENERATE_AND_TEST:
                    print("✓ PySketchFix is started...")
                    SketchMaker.generate_sketches(bug_file, buggy_line)
                    PatchFinder.run_sketches(bug_file, bug_test_file)
        print("#######################################################################################################")
        print("Results with bug numbers:")
        print("Project:" + str(project_to_evaluate))
        print("Failing:" + str(failing_tests_array))
        print("Passing:" + str(passing_tests_array))
        print("Empty Suspicious Lines:" + str(empty_suspicious_lines_array))
        print("No bug information is found:" + str(no_info_or_patch_file_array))
        if GENERATE_RESULT:
            sys.stdout.close()


def clone_git_repo(github_url, git_project_folder):
    """
    :param git_project_folder: The path to the project which is currently evaluated.
    :param github_url: The url to the github repo which has to be cloned.

    :return: True, if the project could be cloned, false otherwise.
    """
    if github_url == "" or git_project_folder == "":
        return False
    print("CLONING PROJECT:")
    if not os.path.exists(git_project_folder):
        print("✓ SUCCESSFUL! This project is cloned: " + github_url)
        os.system("git clone " + github_url + " " + git_project_folder)
    else:
        print("✓ SUCCESSFUL! This project is already cloned: " + github_url)
    if not os.path.exists(git_project_folder):
        print("x FAIL! Could not clone the Repo next Project is taken.")
        return False
    else:
        return True


def reset_git_repo_to_buggy_commit(git_project_folder, buggy_commit_id):
    """
    :param git_project_folder: The path to the project which is currently evaluated.
    :param buggy_commit_id: The buggy commit id to which the project is reset.
    """
    os.system("cd " + git_project_folder + "\n  git reset --hard " + buggy_commit_id)


def open_patch_for_bug_file(bip_bug_patch_file):
    """
    :param bip_bug_patch_file: The information file about the patch for the bug which is currently set.

    :return: the path to the bug file.
    """
    bug_file = ""
    # Search for the line in the bug patch file with the bug file and return it in correct format.
    with open(bip_bug_patch_file, 'r') as file:
        for line in file:
            if line.__contains__("diff --git a/"):
                bug_file = line.replace('diff --git a/', '')
                break
        file.close()
    if bug_file.__contains__("b/"):
        bug_file = bug_file[:bug_file.index(" b/")]
        bug_file = bug_file.replace(' ', '')
    return bug_file


def open_info_for_bug_test_file(bip_bug_info):
    """
    :param bip_bug_info: The information file about the bug which is currently set.

    :return: the path to the test file to the bug file. Important! The test has to be unit test.
    """
    test_file_path = ""
    # Search for the line in the bug info with the test file and return it in correct format.
    with open(bip_bug_info, 'r') as file:
        for line in file:
            if line.__contains__("test_file"):
                test_file_path = line.replace('test_file=', '')
                break
        file.close()
    test_file_path = test_file_path.replace('"', '')
    test_file_path = test_file_path.replace('\n', '')
    test_file_path = test_file_path.replace(' ', '')
    # If there are multiple tests, return the first one which is found.
    if test_file_path.__contains__(";"):
        test_file_path_index = test_file_path.index(";")
        test_file_path = test_file_path[:test_file_path_index]
    return test_file_path


def open_info_for_buggy_commit_id(bip_bug_info):
    """
    :param bip_bug_info: The information file about the bug which is currently set.

    :return: the buggy commit id to the bug file.
    """
    buggy_commit_id = ""
    # Search for the line in the bug info with the buggy commit id and return it in correct format.
    with open(bip_bug_info, 'r') as file:
        for line in file:
            if line.__contains__("buggy_commit_id"):
                buggy_commit_id = line.replace('buggy_commit_id', '')
                break
        file.close()
    buggy_commit_id = buggy_commit_id.replace('"', '')
    buggy_commit_id = buggy_commit_id.replace('=', '')
    buggy_commit_id = buggy_commit_id.replace('\n', '')
    buggy_commit_id = buggy_commit_id.replace(' ', '')
    return buggy_commit_id


def open_info_for_github_url(bip_project_info):
    """
    :param bip_project_info: The information file about the project which is evaluated.

    :return: the url to the github repo which has to be cloned.
    """
    github_url = ""
    # Search for the line with the github url and return the url in correct format.
    with open(bip_project_info, 'r') as file:
        for line in file:
            if line.__contains__("github_url="):
                github_url = line.replace('github_url=', '')
                break
        file.close()
    github_url = github_url.replace('"', '')
    github_url = github_url.replace('\n', '')
    github_url = github_url.replace(' ', '')
    return github_url


def bug_information_file_is_valid(bug_information):
    """
    Check if the patch file of the bug is empty or does not exist.
    :param bug_information: The bug patch file or bug info file where the information about the patch is stored.

    :return False: if the bug information file is not valid and no suspicious lines could be found.
    """
    if bug_information == "":
        return False
    # Check if the file exists.
    is_file = os.path.isfile(bug_information)
    # Open the file and read the lines.
    is_not_empty = False
    with open(bug_information, 'r') as file:
        for _ in file:
            # If the file is not empty the value is true.
            is_not_empty = True
            break
    file.close()
    return is_not_empty and is_file


def get_buggy_lines(folder_numbers, bugs_directory, MAXIMUM_BUG_LINES):
    """
    :param bugs_directory: The directory of the project bugs folder which is evaluated.
    :param folder_numbers: The numbers of folders which are set.
    :param MAXIMUM_BUG_LINES: The number of suspicious lines which should be at least returned.

    :return: an array with all suspicious lines.
    """
    # Then for every folder in the folders, the suspicious lines are set.
    suspicious_lines = []
    for folder_number in folder_numbers:
        print("Suspicious lines to bug" + str(folder_number) + ":")
        # The counter which counts how many suspicious lines are returned is set.
        counter_maximum_suspicious_lines = 0
        # Get the patch file to the bug. There the suspicious lines are set.
        bug_patch_file = os.path.join(bugs_directory, str(folder_number), "bug_patch.txt")
        # If the file does not exist or is empty then
        if not bug_information_file_is_valid(bug_patch_file):
            print("The file is empty or does not exist: " + bug_patch_file)
            print("Not Found")
            suspicious_lines.append("")
        else:
            with open(bug_patch_file, 'r') as file:
                str_file = ""
                start_line = 0
                negative_lines_counter = 0
                positive_lines_counter = 0
                # Check every line in the file and get the '-' lines which are set by git. These are the lines where
                # the line is deleted. So here the line is suspicious.
                for line in file:
                    if line.startswith("@@"):
                        start_index = int(line.index("-")) + 1
                        end_index = int(line.index("+")) - 1
                        start_line = (line[start_index:end_index])
                        start_line = start_line[:start_line.index(",")]
                        start_line = int(start_line)
                        negative_lines_counter = 0
                        positive_lines_counter = 0
                    if line.startswith("- "):
                        deleted_line = start_line + negative_lines_counter - 1 - positive_lines_counter
                        positive_lines_counter = 0
                        counter_maximum_suspicious_lines += 1
                        if counter_maximum_suspicious_lines <= MAXIMUM_BUG_LINES:
                            str_file += str(deleted_line) + ","
                    if line.startswith("+ "):
                        positive_lines_counter += 1
                    negative_lines_counter += 1
                # Set the suspicious line and append it to the array.
                suspicious_line = str_file[:len(str_file) - 1]
                print(suspicious_line)
                suspicious_lines.append(suspicious_line)
            file.close()
    return suspicious_lines


main()
