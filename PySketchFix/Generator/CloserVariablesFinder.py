from Generator.Statement import Statement


def get_closer_variables(suspicious_line_number, code_lines_without_code_annotations, number_of_considered_lines):
    """
    Return all variables in the closer lines area of the line number.

    :param suspicious_line_number: The line number which is changed later with expression transformation.
    :param number_of_considered_lines: The number of closer lines considered in the near area of the suspicious line.
    :param code_lines_without_code_annotations: All the lines of the bug file formatted (without code annotations).
    :return: The variables in the nearest area of the line.
    """
    # The number of closest lines are fetched from the config.
    minimal_line_number = suspicious_line_number - number_of_considered_lines
    maximal_line_number = suspicious_line_number + number_of_considered_lines

    # First of all every line in the bug file (which is in the area) is fetched and added to an array.
    number_of_lines = 0
    lines_to_search_variables = []
    for line in code_lines_without_code_annotations:
        number_of_lines += 1
        if minimal_line_number <= number_of_lines <= maximal_line_number:
            lines_to_search_variables.append(line)

    # Then for every line the method find closer variables for line is called. This method returns all variables
    # of this line. If they are not already in the array of closer variables then they are added and returned at the
    # end of execution.
    closer_variables = []
    for line_to_search in lines_to_search_variables:
        closer_variables_in_lines = Statement.find_closer_variables_for_line(line_to_search)
        for closer_variables_in_line in closer_variables_in_lines:
            duplicate_in_array = False
            for closer_variable in closer_variables:
                if closer_variable == closer_variables_in_line:
                    duplicate_in_array = True
                    break
            if not duplicate_in_array:
                closer_variables.append(closer_variables_in_line)

    # Then the closer_variables are stored to ensure that no duplicates are created later.
    closer_variables = sorted(closer_variables)

    return closer_variables
