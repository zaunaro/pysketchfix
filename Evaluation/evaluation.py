import os
import sys
import unittest

import SketchMaker


def main():
    """
    Here PySketchFix is evaluated! To ensure Evaluating PySketchFix right, Ochiai and Tarantula are not tested. (
    where the bug is identified). The buggy lines (-) where given. This isn't even possible because there is only
    one test suite given.
    """

    PROJECTS_FOLDER = "/Users/daniel/BA_SketchFix_Evaluation/Evaluation/Projects"
    """
    Define the folder where the github projects to evaluate were cloned to. If you don't have cloned the Projects
    don't worry the script does this by itself, if they aren't cloned yet.
    """

    BUGS_IN_PY_FOLDER = '/Users/daniel/BA_SketchFix_Evaluation/Evaluation/BugsInPy/projects'
    """
    Define the folder where the BugsInPy Folder is cloned to. Here it is important to clone the project by yourself.
    """

    START_PY_FIX_WITH_PASSING_TEST = True
    """
    If this value is true, then also bugs which have a passing test suite are started to generate sketches. (They are
    useless because SketchFix thinks that every sketch is a patch because all tests are passing) But for evaluation 
    reasons, to identify the number of possible created sketches I decided to add this function.
    """

    MAXIMUM_BUG_LINES = 5
    """
    Defines the top suspicious lines which are taken to generate sketches. If you would like to add more suspicious 
    lines then feel free, but the runtime will be very slow.
    """

    PROJECTS_TO_EVALUATE = ['black']
    """
    Define the names of the projects which should be evaluated with bugs in py.
    """

    python_interpreter = "/Users/daniel/BachelorarbeitDZ/PySketchFix/venv/bin/python"
    sketch_generator = "/Users/daniel/BachelorarbeitDZ/PySketchFix/SketchMaker.py"
    """
    
    """
    # TODO Hier noch angeben.

    for project_to_evaluate in PROJECTS_TO_EVALUATE:
        # Set the array where the results are stored for this project.
        failing_tests_array = []
        empty_suspicious_lines_array = []
        passing_tests_array = []
        file_not_found_array = []
        # Then fetch the git hub url from the proj folder project.info
        bip_proj_info = BUGS_IN_PY_FOLDER
        bip_proj_info = os.path.join(bip_proj_info, project_to_evaluate, 'project.info')
        if not os.path.exists(bip_proj_info):
            print("FAIL! The project file: " + str(bip_proj_info) + " in the project " + str(project_to_evaluate) +
                  " does not exists. Next proj is taken")
            continue
        github_url = open_git_hub_proj(bip_proj_info)
        print()
        print()
        print()
        print("#######################################################################################################")
        print("                             PROJECT: " + project_to_evaluate)
        print("#######################################################################################################")
        directory = os.path.join(BUGS_IN_PY_FOLDER, project_to_evaluate, "bugs/")

        # Clone the repository in the projects folder if it doesn't exists already.
        GITHUB_REPO_PROJ = os.path.join(PROJECTS_FOLDER, project_to_evaluate)
        print("CLONING PROJECT:")
        if not os.path.exists(GITHUB_REPO_PROJ):
            print("✓ SUCCESSFUL! This project is cloned: " + github_url)
            os.system("git clone " + github_url + " " + GITHUB_REPO_PROJ)
        else:
            print("✓ SUCCESSFUL! This project is already cloned: " + github_url)
        if not os.path.exists(GITHUB_REPO_PROJ):
            print("x FAIL! Could not clone the Repo next Proj is taken.")
            continue

        # Now get the different bugs in bugs in py directory.
        bug_file_infos = get_bug_infos(project_to_evaluate, BUGS_IN_PY_FOLDER)
        if len(bug_file_infos) == 0:
            continue

        # The number of failing an passing test cases to the bugs are counted.
        number_of_failing_test_cases = 0
        number_of_passing_test_cases = 0

        # Find buggy lines
        print(".......................................................................................................")
        print("BUGGY LINES:")
        buggy_lines = get_buggy_lines(directory, MAXIMUM_BUG_LINES)
        print(".......................................................................................................")

        # Now for every bug in the BUGSINPY directory fetch the bug file, the commit and fixing id and the test file.
        number_of_evaluated_bugs = 0
        for bug_file_info in bug_file_infos:
            # At first the bug number is stored.
            bug_number = bug_file_info[0]
            print()
            print(
                "+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+")
            print()
            print("                                          BUG: " + str(bug_number))
            print()
            print(
                "+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+")

            # Then open the bug information to store the buggy commit id.
            buggy_commit_id = open_info_for_buggy_commit_id(bug_file_info[1])
            if buggy_commit_id == "":
                print("x FAIL! The buggy commit id in bug: " + str(bug_number) + " to the project " + str(
                    project_to_evaluate) + " does not exists. Next bug is taken")
                continue

            # Then open the bug information to store the buggy commit id.
            fixed_commit_id = open_info_for_buggy_commit_id(bug_file_info[1])
            if fixed_commit_id == "":
                print("x FAIL! The fixed commit id in bug: " + str(bug_number) + " to the project " + str(
                    project_to_evaluate) + " does not exists. Next bug is taken")
                continue

            number_of_evaluated_bugs += 1
            print("GIT RESET TO: " + buggy_commit_id)
            # Reset the git hub repo to the buggy commit id.
            reset_git_repo_to_buggy_commit(GITHUB_REPO_PROJ, buggy_commit_id)

            # Then the bug test file is fetches with the information.
            bug_test_file = open_info_for_bug_test_file(bug_file_info[1])
            bug_test_file = os.path.join(PROJECTS_FOLDER, project_to_evaluate, bug_test_file)
            if not os.path.isfile(bug_test_file):
                print(
                    "x FAIL! The bug test file: " + str(bug_test_file) + " to the project " + str(project_to_evaluate) +
                    " with bug: " + str(bug_number) + "does not exists. Next bug is taken")
                file_not_found_array.append(bug_number)
                continue

            # Then the bug file itself is fetched.
            bug_file = open_bug_patch_for_file(bug_file_info[2])
            bug_file = os.path.join(PROJECTS_FOLDER, project_to_evaluate, bug_file)
            if not os.path.isfile(bug_test_file):
                print("x FAIL! The bug file: " + str(bug_file) + " to the project " + str(project_to_evaluate) +
                      " with bug: " + str(bug_number) + "does not exists. Next bug is taken")
                file_not_found_array.append(bug_number)
                continue

            # Increment the number of evaluated bugs if everything is setup well.
            print("bug_file = " + str(bug_file))
            print("bug_test_file = " + str(bug_test_file))

            # Now the test file is run to get to know, if the test passes or not.
            print("TEST EXECUTION:")
            loader = unittest.TestLoader()
            VERBOSITY = 2
            UNIT_TEST_FILE_BASENAME = os.path.basename(bug_test_file)
            UNIT_TEST_FILE_DIRECTORY = bug_test_file.replace(UNIT_TEST_FILE_BASENAME, "")
            suite = loader.discover(UNIT_TEST_FILE_DIRECTORY, pattern=UNIT_TEST_FILE_BASENAME)
            runner = unittest.TextTestRunner(sys.stderr, verbosity=VERBOSITY).run(suite)
            print("...........................")
            if len(runner.failures) + len(runner.errors) == 0:
                number_of_passing_test_cases += 1
                print("✓ SUCCESSFUL! TEST PASSES")
                # Get buggy lines:
                bug_number_int = int(bug_number)
                buggy_line = buggy_lines[bug_number_int - 1]
                if len(buggy_line) == 0:
                    print("x FAIL! Suspicious lines are empty!")
                    empty_suspicious_lines_array.append(bug_number_int)
                else:
                    passing_tests_array.append(bug_number_int)
                    if not START_PY_FIX_WITH_PASSING_TEST:
                        print("x PyFix could not be started if test passes...")
                        print()
                    else:
                        print("✓ PyFix is started...")
                        print()
                        SketchMaker.generate_sketches(bug_file, buggy_line)
            else:
                number_of_failing_test_cases += 1
                print("x TEST FAILS")
                # Get buggy lines:
                bug_number_int = int(bug_number)
                buggy_line = buggy_lines[bug_number_int - 1]
                if len(buggy_line) == 0:
                    print("x FAIL! Suspicious lines are empty!")
                    empty_suspicious_lines_array.append(bug_number_int)
                else:
                    failing_tests_array.append(bug_number_int)
                    print("✓ PyFix is started...")
                    print()
                    SketchMaker.generate_sketches(bug_file, buggy_line)
                    # PatchFinder.run_sketches(bug_file, bug_test_file)
        print("#######################################################################################################")
        print("Results with bug numbers:")
        failing_tests_array.sort()
        passing_tests_array.sort()
        empty_suspicious_lines_array.sort()
        print("Project:" + str(project_to_evaluate))
        print("Failing:" + str(failing_tests_array))
        print("Empty Sus Lines: " + str(empty_suspicious_lines_array))
        print("Passing" + str(passing_tests_array))
        print("Not Found" + str(file_not_found_array))


def reset_git_repo_to_buggy_commit(git_proj_folder, buggy_commit_id):
    os.system("cd " + git_proj_folder + "\n  git reset --hard " + buggy_commit_id)


def open_bug_patch_for_file(bug_file_patch):
    bug_file = ""
    with open(bug_file_patch, 'r') as filehandle:
        for line in filehandle:
            if line.__contains__("diff --git a/"):
                bug_file = line.replace('diff --git a/', '')
                break
    if bug_file.__contains__("b/"):
        bug_file = bug_file[:bug_file.index(" b/")]
        bug_file = bug_file.replace(' ', '')
    return bug_file


def open_info_for_buggy_commit_id(bip_bug_info):
    buggy_commit_id = ""
    with open(bip_bug_info, 'r') as filehandle:
        for line in filehandle:
            if line.__contains__("buggy_commit_id"):
                buggy_commit_id = line.replace('buggy_commit_id', '')
                break
    buggy_commit_id = buggy_commit_id.replace('"', '')
    buggy_commit_id = buggy_commit_id.replace('=', '')
    buggy_commit_id = buggy_commit_id.replace('\n', '')
    buggy_commit_id = buggy_commit_id.replace(' ', '')
    return buggy_commit_id


def open_info_for_fixing_commit_id(bip_bug_info):
    fixed_commit_id = ""
    with open(bip_bug_info, 'r') as filehandle:
        for line in filehandle:
            if line.__contains__("fixed_commit_id"):
                fixed_commit_id = line.replace('fixed_commit_id', '')
                break
    fixed_commit_id = fixed_commit_id.replace('=', '')
    fixed_commit_id = fixed_commit_id.replace('"', '')
    fixed_commit_id = fixed_commit_id.replace('\n', '')
    fixed_commit_id = fixed_commit_id.replace(' ', '')
    return fixed_commit_id


def open_info_for_bug_test_file(bip_bug_info):
    test_file_path = ""
    with open(bip_bug_info, 'r') as filehandle:
        for line in filehandle:
            if line.__contains__("test_file"):
                test_file_path = line.replace('test_file=', '')
                break
    test_file_path = test_file_path.replace('"', '')
    test_file_path = test_file_path.replace('\n', '')
    test_file_path = test_file_path.replace(' ', '')
    return test_file_path


def open_git_hub_proj(bip_proj_info):
    github_url = ""
    with open(bip_proj_info, 'r') as filehandle:
        for line in filehandle:
            if line.__contains__("github_url="):
                github_url = line.replace('github_url=', '')
                break
    github_url = github_url.replace('"', '')
    github_url = github_url.replace('\n', '')
    github_url = github_url.replace(' ', '')
    return github_url


def get_bug_infos(project_to_evaluate, BUGS_IN_PY_FOLDER):
    # First of all the projects to evaluate has to be found in bugs in py:
    bip_bugs_to_project = os.path.join(BUGS_IN_PY_FOLDER, project_to_evaluate, 'bugs')

    # If the folder does not exists then a message is printed and the next project is taken.
    if not os.path.exists(bip_bugs_to_project):
        print("The folder: " + str(bip_bugs_to_project) + " to the project " + str(project_to_evaluate) +
              " does not exists. Next project is taken")
        return []

    # Get the 'numbers' folder of bugs in the bugs folder.
    folders = os.listdir(bip_bugs_to_project)
    folders_number = []
    for folder in folders:
        if str.isnumeric(str(folder)):
            folders_number.append(int(str(folder)))

    # For every folder number in the folders make a new path for the bug info.
    bug_files = []
    folders_number.sort()
    for folder_number in folders_number:
        bip_bugs = os.path.join(str(bip_bugs_to_project), str(folder_number))
        # If the folder does not exists then a message is printed and the next project is taken.
        if not os.path.exists(bip_bugs):
            print("The bug folder: " + str(bip_bugs) + " in the project " + str(project_to_evaluate) +
                  " does not exists. Next bug is taken")
            continue

        bip_bug_info = os.path.join(bip_bugs, 'bug.info')
        if not os.path.isfile(bip_bug_info):
            print("The file: " + str(bip_bug_info) + " in the project " + str(project_to_evaluate) +
                  " does not exists. Next bug is taken")
            continue

        bip_bug_patch = os.path.join(bip_bugs, 'bug_patch.txt')
        if not os.path.isfile(bip_bug_patch):
            print("The file: " + str(bip_bug_patch) + " in the project " + str(project_to_evaluate) +
                  " does not exists. Next bug is taken")
            continue
        bug_files.append([folder_number, bip_bug_info, bip_bug_patch])

    return bug_files


def get_buggy_lines(directory, MAXIMUM_BUG_LINES):
    folders = os.listdir(directory)
    folders_number = []
    for folder in folders:
        if folder.isnumeric():
            folders_number.append(int(folder))

    folders_number.sort()
    buggy_lines = []
    for folder_number in folders_number:
        counter_maximum = 0
        bug_path_file = directory + str(folder_number) + "/bug_patch.txt"
        # print(bug_path_file)
        if not os.path.isfile(bug_path_file):
            print("NF")
            buggy_line = ""
            buggy_lines.append(buggy_line)
        else:
            with open(bug_path_file, 'r') as file:
                str_file = ""
                start_line = 0
                negative_lines_counter = 0
                positive_lines_counter = 0
                for line in file:
                    if line.startswith("@@"):
                        start_index = int(line.index("-")) + 1
                        end_index = int(line.index("+")) - 1
                        start_line = (line[start_index:end_index])
                        start_line = start_line[:start_line.index(",")]
                        start_line = int(start_line)
                        # print("Start_Line:")
                        # print(start_line)
                        negative_lines_counter = 0
                        positive_lines_counter = 0
                    if line.startswith("- "):
                        # print("DeletedLine")
                        deleted_line = start_line + negative_lines_counter - 1 - positive_lines_counter
                        # print(deleted_line)
                        positive_lines_counter = 0
                        counter_maximum += 1
                        if counter_maximum <= MAXIMUM_BUG_LINES:
                            str_file += str(deleted_line) + ","
                    if line.startswith("+ "):
                        positive_lines_counter += 1
                    negative_lines_counter += 1
                print(str_file[:len(str_file) - 1])
                buggy_line = str_file[:len(str_file) - 1]
                buggy_lines.append(buggy_line)
    return buggy_lines


main()
