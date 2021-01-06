import itertools
import os
import sys
import time

from Config import FileHandler
from Config.ConfigReader import ConfigReader
from Generator import CloserVariablesFinder, SketchWriter
from Generator import LineTransformer
from Generator.ListOfSketchContent import ListOfSketchContent
from Generator.SketchWriter import SketchStore
from Generator.TransformedLine import TransformedLine, ListOfTransformedLines
from Schemas.TransformationManager import TransformationManager


def generate_sketches(bug_file, buggy_lines):
    """
    This method starts to create sketches with a number of suspicious lines and a unit testsuite suite.

    :param bug_file: The bug file where patches are find.
    :param buggy_lines: The buggy lines which you can give as system argument.
    :raise RunTimeError: If the suspicious lines are emtpy.
    """
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print()
    print("	                              PySketchFix®: Sketches are created.")
    print()
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    start_time = time.time()
    # Reset the old values.
    SketchStore.number_of_created_sketches = 0
    SketchStore.list_of_created_sketch_content = []

    # Setup the Config directory with the two files which are taken as arguments. The one is the bug file and the
    # other one the unit testsuite file to it. It is also needed where the project is located, to store sketches and
    # patches right, so the project path is taken from this file.
    project_path = os.path.dirname(os.path.abspath(__file__))
    ConfigReader.setup_environment_for_SketchMaker(bug_file, project_path)
    print("PySketchFix will run with:\nbug file: " + bug_file)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    # Delete all recent created sketches but not the cache and init files. Therefore the config parameter sketch
    # directory is checked.
    SKETCH_DIRECTORY = str(ConfigReader.get_sketch_directory())
    for filename in os.listdir(SKETCH_DIRECTORY):
        if not filename.__contains__("__pycache__") and not filename == "__init__.py":
            os.remove(os.path.join(SKETCH_DIRECTORY, filename))

    # Now the lines of the code are parsed with the File Parser and the length stored.
    # Here also in every line the code annotations are removed, to ensure the statement can parse the line. This is done
    # for all lines, because the statement parses lines above or around the are of the buggy lines, to get the values.
    code_lines = FileHandler.parse_file_for_content_as_array(ConfigReader.get_bug_file())
    number_of_code_lines = len(code_lines)
    code_lines_without_annotations = []
    for code_line in code_lines:
        code_lines_without_annotations.append(LineTransformer.remove_code_annotations(code_line))

    # First of all is checked if buggy lines are given by the user. If so they will be extracted in an array.
    suspicious_line_numbers = []
    if buggy_lines != "":
        arr = buggy_lines.split(',')
        for number in arr:
            if str.isnumeric(number):
                suspicious_line_numbers.append(int(number))

    # Check if the suspicious lines are empty then stop the execution.
    if len(suspicious_line_numbers) == 0:
        raise RuntimeError(
            "The suspicious lines you want to take are empty or not valid: " + str(suspicious_line_numbers))
    else:
        suspicious_line_numbers.sort()
        print("The suspicious lines which are taken are: " + str(suspicious_line_numbers))
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        # This array stores every possible line transformation. This array is as long as the code is in the bug file.
        # Now every line number in the buggy file is taken and a transformation is done, if the line number is in the
        # suspicious lines.
        collection = []
        # Count the number of lines which could not be transformed and add it in to an array.
        suspicious_lines_without_transformation = []
        for line_number in range(1, number_of_code_lines + 1):
            # First of all the original code line and this line without code_line_annotations is fetched.
            original_code_line = code_lines[line_number - 1]
            original_code_line_without_annotations = code_lines_without_annotations[line_number - 1]

            # Then a list of possible transformations of the line is created. Therefore at the beginning,
            # the original code line is appended in the list. (To ensure that at least one line content is in the array)
            list_of_line_transformations = ListOfTransformedLines(line_number,
                                                                  original_code_line,
                                                                  original_code_line_without_annotations)

            # If the line number is in the suspicious lines then a transformation is created and added in the array.
            if line_number in suspicious_line_numbers:
                list_of_line_transformations = generate_transformations_for_line(line_number,
                                                                                 original_code_line,
                                                                                 original_code_line_without_annotations,
                                                                                 list_of_line_transformations,
                                                                                 code_lines_without_annotations)
                # If the list of line transformations contains only one member then there is only the original line in
                # it.
                if len(list_of_line_transformations.transformed_lines) == 1:
                    suspicious_lines_without_transformation.append(line_number)
                    print("x Fail! Line: " + str(
                        line_number) + " could not be transformed: '" + original_code_line_without_annotations + "'")
                else:
                    print("✓")

            # Add the list to an array.
            collection.append(list_of_line_transformations)

        # Then create the sketch file contents and write the sketches in a file.
        create_sketch_file_contents(collection, code_lines)

        # At the end the statistics are written on the console.
        SketchWriter.print_statistics(suspicious_lines_without_transformation)
        print("Time needed: " + str(round(((time.time() - start_time) / 60), 2)) + " minutes.")


def generate_transformations_for_line(suspicious_line_number, suspicious_code_line,
                                      suspicious_code_line_without_annotations, list_of_line_transformations,
                                      code_lines_without_annotations):
    """
    Generate transformations for a suspicious lines and add it into the given list.

    :param suspicious_line_number: The line number which is currently suspicious.
    :param suspicious_code_line: The concrete line of the line number.
    :param suspicious_code_line_without_annotations: The concrete line of the line number without annotations.
    :param list_of_line_transformations:  The list of line transformations where the transformations are added.
    :param code_lines_without_annotations: The whole array of suspicious lines without annotations to get the closer
    variables.
    :return the modified list of line transformations.
    """
    # Print an information for the user.
    print("Start transforming line: " + str(suspicious_line_number))
    # The depth array defines how deep the tree of statements is parsed for transformation.
    DEPTH_ARRAY = ConfigReader.get_depth()

    # The transformation schema combinations which are done for every sketch with suspicious lines.
    TRANSFORMATION_SCHEMA_COMBINATIONS = ConfigReader.get_transformation_schema_combinations()

    # The considered lines of the expression transformation, which are the variables considered in the area of the
    # transformation.
    CONSIDERED_LINES = ConfigReader.get_considered_lines_variables()

    for considered_line in CONSIDERED_LINES:
        # For every considered line in the array, the closer variables are fetched.
        closer_variables = CloserVariablesFinder.get_closer_variables(suspicious_line_number,
                                                                      code_lines_without_annotations,
                                                                      considered_line)

        # Then for this line every transformation schema combination is applied.
        for transformation_schemas in TRANSFORMATION_SCHEMA_COMBINATIONS:

            # Because you can go in the transformations as deep as you wish, for every depth in the depth array
            # a transformation is applied.
            for depth in DEPTH_ARRAY:
                try:
                    transformation = LineTransformer.transform_line(transformation_schemas,
                                                                    depth,
                                                                    suspicious_code_line_without_annotations,
                                                                    suspicious_line_number,
                                                                    closer_variables)
                finally:
                    # After execution delete the number of transformations done.
                    TransformationManager.clear_number_of_transformations()

                # If there is no transformation then the transformed line is not stored, otherwise a transformed
                # line object is created, where the transformation is stored and then added into the list.
                if transformation != "":
                    transformed_line = TransformedLine(suspicious_line_number,
                                                       suspicious_code_line,
                                                       suspicious_code_line_without_annotations,
                                                       transformation)
                    list_of_line_transformations.add_transformed_line(transformed_line)
    return list_of_line_transformations


def create_sketch_file_contents(collection, code_lines):
    # The whole string of the bug file.
    code_lines_str = FileHandler.parse_file_for_content_as_string(ConfigReader.get_bug_file())
    list_of_sketch_content = ListOfSketchContent(code_lines_str)

    # Now a content array is created. Therefore is checked if a line number is suspicious or not. If it is, then
    # an empty array is appended. Otherwise the original line of the code is appended in an array.
    content_array = []
    number_of_lines = 1
    for _ in code_lines:
        transformations_to_line = []
        list_of_transformed_lines = collection[number_of_lines - 1]
        transformed_lines = list_of_transformed_lines.transformed_lines
        for transformed_line in transformed_lines:
            transformations_to_line.append(transformed_line.transformed_original_code_line)
        number_of_lines += 1
        content_array.append(transformations_to_line)

    # Now every possible combination is done. Therefore itertools is used. This is copied by
    # https://www.daniweb.com/programming/software-development/threads/272967/array-of-arrays-for-itertools-product.
    list_of_possible_combinations = list(itertools.product(*content_array))

    # Then the combinations of the lines are parsed and appended to each other and added to the list of sketch content.
    for list_of_lines in list_of_possible_combinations:
        content = ''
        for line in list_of_lines:
            content += line
        list_of_sketch_content.add_content(content)

    # For every content in the list the sketch is written.
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Start creating " + str(len(list_of_sketch_content.contents)) + " sketches.")
    for content in list_of_sketch_content.contents:
        SketchWriter.write_sketch(content)
    print("✓")


# Check the arguments of the user input.
if __name__ == "__main__":
    if len(sys.argv) == 3:
        bug_file_input = str(sys.argv[1])
        buggy_lines_input = str(sys.argv[2])
        generate_sketches(bug_file_input, buggy_lines_input)
    else:
        print("xPlease give arguments: bug file and the suspicious lines as 1,2,3")
