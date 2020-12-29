class Hole(object):
    """
    A hole defines the transformation done in the code. Therefore it contains the information about the changed code,
    the number and line where the hole in the code is and the type of transformation done. The value of the code is also
    stored to get the information about the hole in later testsuite executions.
    """

    def __init__(self, hole_number, line, array_of_changed_code, transformation_type, varoperator):
        """
        :param hole_number: to identify the hole in the code.
        :param line: where the changed code in the bug file was.
        :param array_of_changed_code: an array with changed code (here e.g. a == b and b == a) are in it to make sure
        that both variations are possible and to get not many redundant holes.
        :param transformation_type: the transformation done.
        :param varoperator: the variable or operator of the hole is the outcome of the changed code
        """
        self.hole_number = hole_number
        self.line = line
        self.array_of_changed_code = array_of_changed_code
        self.transformation_type = transformation_type
        self.varoperator = varoperator

    def is_equal(self, other):
        """
        Check if a hole is equal to another one. Here the value (value) is also compared.

        :param other: the other hole which is compared.
        :return: True if they are equal, false otherwise.
        """
        if not self.varoperator == other.varoperator:
            return False
        return self.has_equal_changed_code(other)

    def has_equal_changed_code(self, other):
        """
        Checks if the other hole has the same parameters (information) about the hole, line, changed code but not the
        value. This is needed to compare later the different executions of holes. They have different outcome and this
        is analyzed later after testsuite executions.

        :param other: the other hole which is compared.
        :return: True if they are equal, false otherwise.
        """
        if not self.hole_number == other.hole_number:
            return False
        if not self.line == other.line:
            return False
        if not str.__eq__(self.transformation_type, other.transformation_type):
            return False
        if not len(self.array_of_changed_code) == len(other.array_of_changed_code):
            return False
        self.array_of_changed_code.sort()
        other.array_of_changed_code.sort()
        if not self.array_of_changed_code == other.array_of_changed_code:
            return False
        return True

    def to_array(self):
        """
        :return: The hole number, line, list of changed code and the transformation type of the hole in an array.
        """
        return [self.hole_number, self.line, self.array_of_changed_code, self.transformation_type]

    def to_output_format(self):
        """
        :return: A String which is the content of the hole, this content is parsed in the FileHandler.
        """
        content = "Hole:" + str(self.hole_number) + "\n"
        content += "Line:" + str(self.line) + "\n"
        content += "Type:" + str(self.transformation_type) + "\n"
        content += "ChangedCode:" + str(self.array_of_changed_code) + "\n"
        content += "Varoperator:" + str(self.varoperator)
        return content

    def to_patch_format(self):
        """
        :return: A String which is the content of the output file later.
        """
        content = "Hole: " + str(self.hole_number) + " in Line: " + str(self.line) + " with Type: "
        content += str(self.transformation_type) + " has following changed code: " + str(self.array_of_changed_code)
        return content
