from Config.ConfigReader import ConfigReader
from Generator.Statement import Statement


def remove_code_annotations(line_to_transform):
    """
    Formats the line to transform of the code, where tabulators elif, if etc are listed. These could not be
    evaluated by ast, so they were removed.

    :param line_to_transform: The line in the code which should be analysed by ast.
    :return: The changed line without: \t, \n, if, else, elif, for, while etc.
    """
    line_to_transform = str(line_to_transform)
    line_to_transform = line_to_transform.split(' #', 1)[0]
    line_to_transform = line_to_transform.replace(':', '')
    line_to_transform = line_to_transform.replace('\t', '')
    line_to_transform = line_to_transform.replace('    ', '')
    line_to_transform = line_to_transform.replace('\n', '')
    line_to_transform = line_to_transform.replace('elif ', '')
    line_to_transform = line_to_transform.replace('if ', '')
    line_to_transform = line_to_transform.replace('else ', '')
    line_to_transform = line_to_transform.replace('else', '')
    line_to_transform = line_to_transform.replace('def ', '')
    line_to_transform = line_to_transform.replace('for ', '')
    line_to_transform = line_to_transform.replace('while ', '')
    return line_to_transform


def transform_line(transformation_schemas, depth, code_line_without_annotations, line_number, closer_variables):
    """
    This method transforms a line with all transformation schema it gets. Therefore it needs the code line without
    code annotations to parse the statement, the line number where the bug is located and the closer variables, for the
    expression transformations. The depth is used to check how deep the ast tree is parsed and transformations are
    applied.

    :param code_line_without_annotations: The line which should be transformed.
    :param line_number: The line number where the line is located.
    :param depth: How deep the ast tree is parsed.
    :param closer_variables: The closer variables in the area of the line number.
    :param transformation_schemas: The transformation schemas which are applied at once.
    :return: the transformation, ("" if no transformation could be done).
    """
    # First of all the line has to be parsed by the statement. Here no import statements could be parsed.
    if code_line_without_annotations.__contains__("import"):
        if ConfigReader.get_debug_mode():
            print("Line contains import statement.")
        return ""
    statement = Statement.parse_line_to_statement(code_line_without_annotations)
    if statement is None:
        if ConfigReader.get_debug_mode():
            print("Statement to line: " + code_line_without_annotations + " could not be parsed by ast.")
        return ""

    # If the expression transformation is the only schema then don't call the other method where the other schemas
    # are applied. If there are other schemas, then (if the expression transformation is in it) it will be applied
    # automatically. But if it is alone, then the other method does not work.
    if 'EXP' in transformation_schemas and len(transformation_schemas) == 1:
        statement.change_to_exp_transformation(line_number, depth, closer_variables)
    else:
        statement.change_to_transformation(transformation_schemas, line_number, depth, closer_variables)

    # Check if the transformation is the same as the input, then no transformation could be applied:
    transformation = str(statement.transformation)
    if transformation == "" or transformation == code_line_without_annotations:
        if ConfigReader.get_debug_mode():
            print("Transformation is empty or the same as the code line: " + transformation)
        return ""
    else:
        return transformation
