from Schemas import ExpressionTransformation, ComparisonTransformation, LogicalTransformation, \
    ArithmeticTransformation


class TransformationManager(object):
    """
    The Transformation Manager creates new transformations and clears the holes of every transformation. Here the
    number of transformations for each sketch is hold.
    """
    number_of_transformations = 0

    @staticmethod
    def clear_current_holes():
        """
        Clear the current holes in every transformation after a testsuite execution (iteration).
        """
        ExpressionTransformation.EXPTransformation.clear_current_holes()
        ComparisonTransformation.COMTransformation.clear_current_holes()
        LogicalTransformation.LOGTransformation.clear_current_holes()
        ArithmeticTransformation.ARITransformation.clear_current_holes()

    @staticmethod
    def clear_number_of_transformations():
        """
        The number of transformations is deleted. This is done after a sketch is created.
        """
        TransformationManager.number_of_transformations = 0

    @staticmethod
    def create_transformation(transformation_type, line_number, parent, left_operand, right_operand):
        """
        Here the arrays for the hole were created. At the first position of the array is the name of the operand. At
        the second position of the array is the value of the operand. This is only done if the left or right operand
        is not a transformation.

        :param transformation_type: The type of the transformation.
        :param line_number: The line where the transformation is.
        :param parent: If the transformation has a parent this value is true.
        :param left_operand: the left operand of the logical, comparison and arithmetic operation as string.
        :param right_operand: the right operand of the logical, comparison and arithmetic operation as string.
        :return: the transformation as string.
        :raise RuntimeError if the type of the creation is expression.
        """
        if not (transformation_type == 'LOG' or transformation_type == 'ARI' or transformation_type == 'COM'):
            raise RuntimeError("EXP Transformation could not be called with createTransformation.")

        # Check if the operand contains a Transformation. This is the case, when a Transformation contains another
        # Transformation.
        if not str(left_operand).__contains__("Transformation"):
            left_value_array = "[\'" + left_operand + "\', " + left_operand + "]"
        else:
            left_value_array = left_operand
        if not str(right_operand).__contains__("Transformation"):
            right_value_array = "[\'" + right_operand + "\', " + right_operand + "]"
        else:
            right_value_array = right_operand

        # Increment the number of numberOfTransformations and initialize the hole number, then build the new string.
        TransformationManager.number_of_transformations += 1
        hole_number = TransformationManager.number_of_transformations
        transformation = transformation_type + "Transformation.call(" + str(hole_number) + ", " + str(
            line_number) + ", " + str(parent) + ", " + left_value_array + ", " + right_value_array + ")"
        return transformation

    @staticmethod
    def create_EXP_transformation(line_number, parent, closer_variables):
        """
        Every String representation in the closer variables is appended to the array at first as String representation.
        Then as single variable which has later an assignment while sketch execution e.g: ["a",a].

        :param line_number: The line where the transformation is.
        :param parent: If the transformation has a parent this value is true.
        :param closer_variables: The variables which are in the nearest point of the line.
        :return: the transformation as string.
        :raise RuntimeError: if the closer variables are empty.
        """
        # If the closer variables are empty no transformation could be created.
        if len(closer_variables) == 0:
            return RuntimeError("No expression transformation can be created at line:" + str(
                line_number) + " because the number of closer variables is empty.")

        # The variables have to be appended twice as string and as value (for the code). So here the "'" annotation
        # is first appended and then later removed.
        array = []
        number_of_variables = 0
        has_false_variable = False
        has_true_variable = False
        for variable in closer_variables:
            if variable == 'True':
                has_true_variable = True
            if variable == 'False':
                has_false_variable = True
            array.append([])
            array[number_of_variables].append(variable)
            array[number_of_variables].append('PY_SKETCHFIX_REPLACE' + variable + 'PY_SKETCHFIX_REPLACE')
            number_of_variables = number_of_variables + 1

        # This is needed to ensure that (if there are bool variables) both variations occur.
        if has_true_variable and not has_false_variable:
            array.append(['False', 'PY_SKETCHFIX_REPLACEFalsePY_SKETCHFIX_REPLACE'])
        if has_false_variable and not has_true_variable:
            array.append(['True', 'PY_SKETCHFIX_REPLACETruePY_SKETCHFIX_REPLACE'])

        # Increment the number of number of transformations done and then the string is build.
        TransformationManager.number_of_transformations += 1
        hole_number = TransformationManager.number_of_transformations
        exp_transformation = "EXPTransformation.call(" + str(hole_number) + ", " + str(line_number) + ", " + str(
            parent) + ", " + array.__str__() + ")"

        # Replace the "" assignments in the variables and return the value.
        exp_transformation = exp_transformation.replace("PY_SKETCHFIX_REPLACE'", "")
        exp_transformation = exp_transformation.replace("'PY_SKETCHFIX_REPLACE", "")
        return exp_transformation
