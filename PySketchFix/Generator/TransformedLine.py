class TransformedLine(object):
    """
    The class TransformedLine stores the transformations which are created and compares it with each other, so no
    duplicate transformations or even no transformation is created.
    """

    def __init__(self, line_number, line, line_without_annotations, transformation):
        """
        The creation of a transformed line where the transformations are stored. Here also the original code line
        is replaced with the transformation.

        :param line_number: The line number which is worked with.
        :param line: The original code line.
        :param line_without_annotations: The code line without any annotations.
        :param transformation: The transformation which is done.
        """
        self.line_number = line_number
        self.line = line
        self.line_without_annotations = line_without_annotations
        self.transformation = transformation

        # Replace the transformation with the original code line if the transformation is not empty.
        if transformation != '' or line_without_annotations != '':
            self.transformed_original_code_line = line.replace(line_without_annotations, transformation)
        else:
            self.transformed_original_code_line = line

    def is_equal(self, other):
        """
        Compares two Transformed Lines with each other.

        :param other: The other transformed line.
        :return: True, if the transformed lines are equal, false otherwise.
        """
        if not self.line_number == other.line_number:
            return False
        if not str.__eq__(self.line, other.line):
            return False
        if not str.__eq__(self.transformation, other.transformation):
            return False
        if not str.__eq__(self.transformed_original_code_line, other.transformed_original_code_line):
            return False
        if not str.__eq__(self.line_without_annotations, other.line_without_annotations):
            return False
        return True


class ListOfTransformedLines(object):
    """
    This list stores every possible line transformation to one line.
    """

    def __init__(self, line_number, original_code_line, original_code_line_without_annotations):
        """
        Create a list for each line in the code, where all possible transformations are stored. To make sure that at
        least one transformation is in the list, the original code line is appended as transformed line.

        :param line_number: The line number of the current line.
        :param original_code_line: The original code line to make at least one element in the code.
        :param original_code_line_without_annotations: The original code line without annotations to make at least one
        element in the code.
        """
        self.line_number = line_number
        self.transformed_lines = []
        original_transformed_Line = TransformedLine(line_number, original_code_line,
                                                    original_code_line_without_annotations,
                                                    original_code_line_without_annotations)
        self.transformed_lines.append(original_transformed_Line)

    def add_transformed_line(self, new_transformed_line):
        """
        Add a new transformed line into the array (without duplicates).

        :param new_transformed_line: The new transformed line to append in the array.
        """
        has_duplicate = False
        for transformed_line in self.transformed_lines:
            if transformed_line.is_equal(new_transformed_line):
                has_duplicate = True
                break
        if not has_duplicate:
            self.transformed_lines.append(new_transformed_line)
