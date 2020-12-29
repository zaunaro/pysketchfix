import unittest

from Generator.Statement import Statement
from Schemas.TransformationManager import TransformationManager


class TestStatement(unittest.TestCase):
    """
    Tests the Statement.py script in the Generator.Statement.
    """

    @staticmethod
    def check_statement_string(line, statement_solution):
        """
        Test the statement string as array.

        :param line: The line which is parsed to statement.
        :param statement_solution: The solution of the array of the created statement.
        :return: the statement which is created if the test does not fail.
        """
        print("#########################################")
        print(line)
        statement = Statement.parse_line_to_statement(line)
        statement_array = str(statement.to_array())
        print(statement_array)
        assert statement_array == statement_solution
        return statement

    @staticmethod
    def check_exp_transformation(statement, statement_transformation_solution):
        """
        Test the statement to transform in an expression transformation.

        :param statement: The statement where the transformation is applied.
        :param statement_transformation_solution: The solution of the transformed statement.
        :return: the statement which is created if the test does not fail.
        """
        print("..........................................")
        print("EXP")
        print("..........................................")
        closer_variables = ['1', '0']
        statement.change_to_exp_transformation(1, 100, closer_variables)
        statement_array = str(statement.transformation)
        print("Actual:")
        print(statement_array)
        print("Expected:")
        print(statement_transformation_solution)
        assert statement_array == statement_transformation_solution
        return statement

    @staticmethod
    def check_transformation(statement, statement_transformation_solution, transformation_schemas):
        """
        Test the statement to transform in an transformation of the given transformation schemas list.

        :param statement: The statement where the transformation is applied.
        :param statement_transformation_solution: The solution of the transformed statement.
        :param transformation_schemas: The transformation schemas which are applied.
        :return: the statement which is created if the test does not fail.
        """
        print("..........................................")
        print(transformation_schemas)
        print("..........................................")
        closer_variables = ['1', '0']
        statement.change_to_transformation(transformation_schemas, 1, 100, closer_variables)
        statement_array = str(statement.transformation)
        print("Actual:")
        print(statement_array)
        print("Expected:")
        print(statement_transformation_solution)
        assert statement_array == statement_transformation_solution
        return statement

    def test_01(self):
        """
        Test an assignment of two variables.
        """
        line = "a = b"
        statement_solution = "['Assign', 'a = b', 'a = b', '=', [['Name', 'a', 'a'], ['Name', 'b', 'b']]]"
        statement = self.check_statement_string(line, statement_solution)
        statementTransformationSolution = "a = EXPTransformation.call(2, 1, False, [['1', 1], ['0', 0]])"
        self.check_exp_transformation(statement, statementTransformationSolution)

    def test_02(self):
        """
        Test an assignment of a variable and a constant.
        """
        line = "a = 1.23232"
        statementSolution = "['Assign', 'a = 1.23232', 'a = 1.23232', '=', [['Name', 'a', 'a'], ['Num', '1.23232', '1.23232']]]"
        statement = self.check_statement_string(line, statementSolution)
        statementTransformationSolution = "a = EXPTransformation.call(4, 1, False, [['1', 1], ['0', 0]])"
        self.check_exp_transformation(statement, statementTransformationSolution)

    def test_03(self):
        """
        Test a return value.
        """
        line = "return False"
        statementSolution = "['Return', 'return False', 'return False', 'return', [['NameConstant', 'False', 'False']]]"
        statement = self.check_statement_string(line, statementSolution)
        statementTransformationSolution = "return EXPTransformation.call(5, 1, False, [['1', 1], ['0', 0]])"
        self.check_exp_transformation(statement, statementTransformationSolution)

    def test_04(self):
        """
        Test a condition between two variables.
        """
        line = "a == b"
        statementSolution = "['Compare', 'a == b', 'a == b', '==', [['Name', 'a', 'a'], ['Name', 'b', 'b']]]"
        statement = self.check_statement_string(line, statementSolution)
        TransformationManager.clear_number_of_transformations()
        statementTransformationSolution = "(EXPTransformation.call(1, 1, False, [['1', 1], ['0', 0]]) == EXPTransformation.call(2, 1, False, [['1', 1], ['0', 0]]))"
        self.check_exp_transformation(statement, statementTransformationSolution)
        TransformationManager.clear_number_of_transformations()
        statementTransformationSolution = "COMTransformation.call(1, 1, False, EXPTransformation.call(1, 1, False, [['1', 1], ['0', 0]]), EXPTransformation.call(2, 1, False, [['1', 1], ['0', 0]]))"
        self.check_transformation(statement, statementTransformationSolution, ["COM"])

    def test_05(self):
        """
        Test an assignment of two variables.
        """
        line = "a += g"
        statementSolution = "['AugAssign', 'a += g', 'a += g', '+=', [['Name', 'a', 'a'], ['Name', 'g', 'g']]]"
        statement = self.check_statement_string(line, statementSolution)
        statementTransformationSolution = "a += EXPTransformation.call(3, 1, False, [['1', 1], ['0', 0]])"
        self.check_exp_transformation(statement, statementTransformationSolution)

    def test_06(self):
        """
        Test a condition with arithmetic transformations done on the left side.
        """
        line = "(a + (b - c)) - ((c / d) * (e % f)) == g"
        statementSolution = "['Compare', '(a + (b - c)) - ((c / d) * (e % f)) == g', '(a + (b - c)) - ((c / d) * (e % f)) == g', '==', [['BinOp', '(a + (b - c)) - ((c / d) * (e % f))', '(a + (b - c)) - ((c / d) * (e % f))', '-', [['BinOp', 'a + (b - c)', 'a + (b - c)', '+', [['Name', 'a', 'a'], ['BinOp', 'b - c', 'b - c', '-', [['Name', 'b', 'b'], ['Name', 'c', 'c']]]]], ['BinOp', '(c / d) * (e % f)', '(c / d) * (e % f)', '*', [['BinOp', 'c / d', 'c / d', '/', [['Name', 'c', 'c'], ['Name', 'd', 'd']]], ['BinOp', 'e % f', 'e % f', '%', [['Name', 'e', 'e'], ['Name', 'f', 'f']]]]]]], ['Name', 'g', 'g']]]"
        statement = self.check_statement_string(line, statementSolution)
        statementTransformationSolution = "(((EXPTransformation.call(4, 1, False, [['1', 1], ['0', 0]]) + (EXPTransformation.call(5, 1, False, [['1', 1], ['0', 0]]) - EXPTransformation.call(6, 1, False, [['1', 1], ['0', 0]]))) - ((EXPTransformation.call(7, 1, False, [['1', 1], ['0', 0]]) / EXPTransformation.call(8, 1, False, [['1', 1], ['0', 0]])) * (EXPTransformation.call(9, 1, False, [['1', 1], ['0', 0]]) % EXPTransformation.call(10, 1, False, [['1', 1], ['0', 0]])))) == EXPTransformation.call(11, 1, False, [['1', 1], ['0', 0]]))"
        self.check_exp_transformation(statement, statementTransformationSolution)
        statementTransformationSolution = "COMTransformation.call(12, 1, False, ((EXPTransformation.call(4, 1, False, [['1', 1], ['0', 0]]) + (EXPTransformation.call(5, 1, False, [['1', 1], ['0', 0]]) - EXPTransformation.call(6, 1, False, [['1', 1], ['0', 0]]))) - ((EXPTransformation.call(7, 1, False, [['1', 1], ['0', 0]]) / EXPTransformation.call(8, 1, False, [['1', 1], ['0', 0]])) * (EXPTransformation.call(9, 1, False, [['1', 1], ['0', 0]]) % EXPTransformation.call(10, 1, False, [['1', 1], ['0', 0]])))), EXPTransformation.call(11, 1, False, [['1', 1], ['0', 0]]))"
        self.check_transformation(statement, statementTransformationSolution, ["COM"])
        statementTransformationSolution = "(ARITransformation.call(18, 1, True, ARITransformation.call(14, 1, True, EXPTransformation.call(4, 1, False, [['1', 1], ['0', 0]]), ARITransformation.call(13, 1, True, EXPTransformation.call(5, 1, False, [['1', 1], ['0', 0]]), EXPTransformation.call(6, 1, False, [['1', 1], ['0', 0]]))), ARITransformation.call(17, 1, True, ARITransformation.call(15, 1, True, EXPTransformation.call(7, 1, False, [['1', 1], ['0', 0]]), EXPTransformation.call(8, 1, False, [['1', 1], ['0', 0]])), ARITransformation.call(16, 1, True, EXPTransformation.call(9, 1, False, [['1', 1], ['0', 0]]), EXPTransformation.call(10, 1, False, [['1', 1], ['0', 0]])))) == EXPTransformation.call(11, 1, False, [['1', 1], ['0', 0]]))"
        self.check_transformation(statement, statementTransformationSolution, ["ARI"])
        statementTransformationSolution = "COMTransformation.call(25, 1, False, ARITransformation.call(24, 1, True, ARITransformation.call(20, 1, True, EXPTransformation.call(4, 1, False, [['1', 1], ['0', 0]]), ARITransformation.call(19, 1, True, EXPTransformation.call(5, 1, False, [['1', 1], ['0', 0]]), EXPTransformation.call(6, 1, False, [['1', 1], ['0', 0]]))), ARITransformation.call(23, 1, True, ARITransformation.call(21, 1, True, EXPTransformation.call(7, 1, False, [['1', 1], ['0', 0]]), EXPTransformation.call(8, 1, False, [['1', 1], ['0', 0]])), ARITransformation.call(22, 1, True, EXPTransformation.call(9, 1, False, [['1', 1], ['0', 0]]), EXPTransformation.call(10, 1, False, [['1', 1], ['0', 0]])))), EXPTransformation.call(11, 1, False, [['1', 1], ['0', 0]]))"
        self.check_transformation(statement, statementTransformationSolution, ["COM", "ARI"])

    def test_07(self):
        """
        Test a condition with an arithmetic operation done on the left side.
        """
        line = "number % element == 0"
        statementSolution = "['Compare', 'number % element == 0', 'number % element == 0', '==', [['BinOp', 'number % element', 'number % element', '%', [['Name', 'number', 'number'], ['Name', 'element', 'element']]], ['Num', '0', '0']]]"
        statement = self.check_statement_string(line, statementSolution)
        statementTransformationSolution = "((EXPTransformation.call(26, 1, False, [['1', 1], ['0', 0]]) % EXPTransformation.call(27, 1, False, [['1', 1], ['0', 0]])) == EXPTransformation.call(28, 1, False, [['1', 1], ['0', 0]]))"
        self.check_exp_transformation(statement, statementTransformationSolution)
        statementTransformationSolution = "COMTransformation.call(29, 1, False, (EXPTransformation.call(26, 1, False, [['1', 1], ['0', 0]]) % EXPTransformation.call(27, 1, False, [['1', 1], ['0', 0]])), EXPTransformation.call(28, 1, False, [['1', 1], ['0', 0]]))"
        self.check_transformation(statement, statementTransformationSolution, ["COM"])
        statementTransformationSolution = "(ARITransformation.call(30, 1, True, EXPTransformation.call(26, 1, False, [['1', 1], ['0', 0]]), EXPTransformation.call(27, 1, False, [['1', 1], ['0', 0]])) == EXPTransformation.call(28, 1, False, [['1', 1], ['0', 0]]))"
        self.check_transformation(statement, statementTransformationSolution, ["ARI"])
        statementTransformationSolution = "COMTransformation.call(32, 1, False, ARITransformation.call(31, 1, True, EXPTransformation.call(26, 1, False, [['1', 1], ['0', 0]]), EXPTransformation.call(27, 1, False, [['1', 1], ['0', 0]])), EXPTransformation.call(28, 1, False, [['1', 1], ['0', 0]]))"
        self.check_transformation(statement, statementTransformationSolution, ["COM", "ARI"])

    def test_08(self):
        """
        Test a logical operation.
        """
        line = "b and c"
        statementSolution = "['BoolOp', 'b and c', 'b and c', 'and', [['Name', 'b', 'b'], ['Name', 'c', 'c']]]"
        statement = self.check_statement_string(line, statementSolution)
        statementTransformationSolution = "(EXPTransformation.call(33, 1, False, [['1', 1], ['0', 0]]) and EXPTransformation.call(34, 1, False, [['1', 1], ['0', 0]]))"
        self.check_exp_transformation(statement, statementTransformationSolution)
        statementTransformationSolution = "(EXPTransformation.call(33, 1, False, [['1', 1], ['0', 0]]) and EXPTransformation.call(34, 1, False, [['1', 1], ['0', 0]]))"
        self.check_transformation(statement, statementTransformationSolution, ["COM"])

    def test_09(self):
        """
        Test a logical operation.
        """
        line = "not b and c"
        statementSolution = "['BoolOp', 'not b and c', 'not b and c', 'and', [['UnaryOp', 'not b', 'not b', 'not', [['Name', 'b', 'b']]], ['Name', 'c', 'c']]]"
        statement = self.check_statement_string(line, statementSolution)
        statementTransformationSolution = "(not EXPTransformation.call(35, 1, False, [['1', 1], ['0', 0]]) and EXPTransformation.call(36, 1, False, [['1', 1], ['0', 0]]))"
        self.check_exp_transformation(statement, statementTransformationSolution)
        statementTransformationSolution = "(not EXPTransformation.call(35, 1, False, [['1', 1], ['0', 0]]) and EXPTransformation.call(36, 1, False, [['1', 1], ['0', 0]]))"
        self.check_transformation(statement, statementTransformationSolution, ["COM"])

    def test_10(self):
        """
        Test a logical operation with a comparison.
        """
        line = "not(d >= b)"
        statementSolution = "['UnaryOp', 'not(d >= b)', 'not(d >= b)', 'not', [['Compare', 'd >= b', 'd >= b', '>=', [['Name', 'd', 'd'], ['Name', 'b', 'b']]]]]"
        statement = self.check_statement_string(line, statementSolution)
        statementTransformationSolution = "not (EXPTransformation.call(37, 1, False, [['1', 1], ['0', 0]]) >= EXPTransformation.call(38, 1, False, [['1', 1], ['0', 0]]))"
        self.check_exp_transformation(statement, statementTransformationSolution)
        statementTransformationSolution = "not (EXPTransformation.call(37, 1, False, [['1', 1], ['0', 0]]) >= EXPTransformation.call(38, 1, False, [['1', 1], ['0', 0]]))"
        self.check_transformation(statement, statementTransformationSolution, ["COM"])

    def test_11(self):
        """
        Test a comparison operation with an arithmetic operation on the right side.
        """
        line = "c == b + 1"
        statementSolution = "['Compare', 'c == b + 1', 'c == b + 1', '==', [['Name', 'c', 'c'], ['BinOp', 'b + 1', 'b + 1', '+', [['Name', 'b', 'b'], ['Num', '1', '1']]]]]"
        statement = self.check_statement_string(line, statementSolution)
        statementTransformationSolution = "(EXPTransformation.call(39, 1, False, [['1', 1], ['0', 0]]) == (EXPTransformation.call(40, 1, False, [['1', 1], ['0', 0]]) + EXPTransformation.call(41, 1, False, [['1', 1], ['0', 0]])))"
        self.check_exp_transformation(statement, statementTransformationSolution)
        statementTransformationSolution = "COMTransformation.call(42, 1, False, EXPTransformation.call(39, 1, False, [['1', 1], ['0', 0]]), (EXPTransformation.call(40, 1, False, [['1', 1], ['0', 0]]) + EXPTransformation.call(41, 1, False, [['1', 1], ['0', 0]])))"
        self.check_transformation(statement, statementTransformationSolution, ["COM"])
        statementTransformationSolution = "(EXPTransformation.call(39, 1, False, [['1', 1], ['0', 0]]) == ARITransformation.call(43, 1, True, EXPTransformation.call(40, 1, False, [['1', 1], ['0', 0]]), EXPTransformation.call(41, 1, False, [['1', 1], ['0', 0]])))"
        self.check_transformation(statement, statementTransformationSolution, ["ARI"])
        statementTransformationSolution = "COMTransformation.call(45, 1, False, EXPTransformation.call(39, 1, False, [['1', 1], ['0', 0]]), ARITransformation.call(44, 1, True, EXPTransformation.call(40, 1, False, [['1', 1], ['0', 0]]), EXPTransformation.call(41, 1, False, [['1', 1], ['0', 0]])))"
        self.check_transformation(statement, statementTransformationSolution, ["COM", "ARI"])

    def test_12(self):
        """
        Test a logical operation.
        """
        line = "b and not c"
        statementSolution = "['BoolOp', 'b and not c', 'b and not c', 'and', [['Name', 'b', 'b'], ['UnaryOp', 'not c', 'not c', 'not', [['Name', 'c', 'c']]]]]"
        statement = self.check_statement_string(line, statementSolution)
        statementTransformationSolution = "(EXPTransformation.call(46, 1, False, [['1', 1], ['0', 0]]) and not EXPTransformation.call(47, 1, False, [['1', 1], ['0', 0]]))"
        self.check_exp_transformation(statement, statementTransformationSolution)
        statementTransformationSolution = "(EXPTransformation.call(46, 1, False, [['1', 1], ['0', 0]]) and not EXPTransformation.call(47, 1, False, [['1', 1], ['0', 0]]))"
        self.check_transformation(statement, statementTransformationSolution, ["COM"])

    def test_13(self):
        """
        Test a for loop.
        """
        line = "element in range(2, number, t)"
        statementSolution = "['Compare', 'element in range(2, number, t)', 'element in range(2, number, t)', 'in', [['Name', 'element', 'element'], ['Call', 'range(2, number, t)', 'range(2, number, t)', 'range', [['Num', '2', '2'], ['Name', 'number', 'number'], ['Name', 't', 't']]]]]"
        statement = self.check_statement_string(line, statementSolution)
        statementTransformationSolution = "(EXPTransformation.call(48, 1, False, [['1', 1], ['0', 0]]) in range(EXPTransformation.call(49, 1, False, [['1', 1], ['0', 0]]), EXPTransformation.call(50, 1, False, [['1', 1], ['0', 0]]), EXPTransformation.call(51, 1, False, [['1', 1], ['0', 0]])))"
        self.check_exp_transformation(statement, statementTransformationSolution)
        statementTransformationSolution = "COMTransformation.call(52, 1, False, EXPTransformation.call(48, 1, False, [['1', 1], ['0', 0]]), range(EXPTransformation.call(49, 1, False, [['1', 1], ['0', 0]]), EXPTransformation.call(50, 1, False, [['1', 1], ['0', 0]]), EXPTransformation.call(51, 1, False, [['1', 1], ['0', 0]])))"
        self.check_transformation(statement, statementTransformationSolution, ["COM"])

    def test_14(self):
        """
        Test a for loop.
        """
        line = "element in range(2, number)"
        statementSolution = "['Compare', 'element in range(2, number)', 'element in range(2, number)', 'in', [['Name', 'element', 'element'], ['Call', 'range(2, number)', 'range(2, number)', 'range', [['Num', '2', '2'], ['Name', 'number', 'number']]]]]"
        statement = self.check_statement_string(line, statementSolution)
        statementTransformationSolution = "(EXPTransformation.call(53, 1, False, [['1', 1], ['0', 0]]) in range(EXPTransformation.call(54, 1, False, [['1', 1], ['0', 0]]), EXPTransformation.call(55, 1, False, [['1', 1], ['0', 0]])))"
        self.check_exp_transformation(statement, statementTransformationSolution)
        statementTransformationSolution = "COMTransformation.call(56, 1, False, EXPTransformation.call(53, 1, False, [['1', 1], ['0', 0]]), range(EXPTransformation.call(54, 1, False, [['1', 1], ['0', 0]]), EXPTransformation.call(55, 1, False, [['1', 1], ['0', 0]])))"
        self.check_transformation(statement, statementTransformationSolution, ["COM"])

    def test_15(self):
        """
        Test an assertion error.
        """
        line = "raise ValueError(a)"
        statementSolution = "['Raise', 'raise ValueError(a)', 'raise ValueError(a)', 'raise', [['Call', 'ValueError(a)', 'ValueError(a)', 'ValueError', [['Name', 'a', 'a']]]]]"
        statement = self.check_statement_string(line, statementSolution)
        statementTransformationSolution = "raise ValueError(EXPTransformation.call(57, 1, False, [['1', 1], ['0', 0]]))"
        self.check_exp_transformation(statement, statementTransformationSolution)

    def test_16(self):
        """
        Test a method name by overloading.
        """
        line = "methodName(1, 2, a)"
        statementSolution = "['Call', 'methodName(1, 2, a)', 'methodName(1, 2, a)', 'methodName', [['Num', '1', '1'], ['Num', '2', '2'], ['Name', 'a', 'a']]]"
        statement = self.check_statement_string(line, statementSolution)
        statementTransformationSolution = "methodName(EXPTransformation.call(58, 1, False, [['1', 1], ['0', 0]]), EXPTransformation.call(59, 1, False, [['1', 1], ['0', 0]]), EXPTransformation.call(60, 1, False, [['1', 1], ['0', 0]]))"
        self.check_exp_transformation(statement, statementTransformationSolution)

    def test_17(self):
        """
        Test an assignment of an array.
        """
        line = "lines = array[1, 2, 6]"
        statementSolution = "['Assign', 'lines = array[1, 2, 6]', 'lines = array[1, 2, 6]', '=', [['Name', 'lines', 'lines'], ['Subscript', 'array[1, 2, 6]', 'array[1, 2, 6]', 'array', [['Index', '1, 2, 6', '1, 2, 6', 'Index', [['Tuple', '1, 2, 6', '1, 2, 6', ', ', [['Num', '1', '1'], ['Num', '2', '2'], ['Num', '6', '6']]]]]]]]]"
        statement = self.check_statement_string(line, statementSolution)
        statementTransformationSolution = "lines = array[EXPTransformation.call(62, 1, False, [['1', 1], ['0', 0]]), EXPTransformation.call(63, 1, False, [['1', 1], ['0', 0]]), EXPTransformation.call(64, 1, False, [['1', 1], ['0', 0]])]"
        self.check_exp_transformation(statement, statementTransformationSolution)

    def test_18(self):
        """
        Test an assignment of an array.
        """
        line = "lines = array[1]"
        statementSolution = "['Assign', 'lines = array[1]', 'lines = array[1]', '=', [['Name', 'lines', 'lines'], ['Subscript', 'array[1]', 'array[1]', 'array', [['Index', '1', '1', 'Index', [['Num', '1', '1']]]]]]]"
        statement = self.check_statement_string(line, statementSolution)
        statementTransformationSolution = "lines = array[EXPTransformation.call(66, 1, False, [['1', 1], ['0', 0]])]"
        self.check_exp_transformation(statement, statementTransformationSolution)

    def test_19(self):
        """
        Test an attribute assignment.
        """
        line = "b = self._VALID_URL"
        statement_solution = "['Assign', 'b = self._VALID_URL', 'b = self._VALID_URL', '=', [['Name', 'b', 'b'], ['Attribute', 'self._VALID_URL', 'self._VALID_URL', None, [['Name', 'self', 'self']]]]]"
        statement = self.check_statement_string(line, statement_solution)
        statementTransformationSolution = "b = self.EXPTransformation.call(68, 1, False, [['1', 1], ['0', 0]])"
        self.check_exp_transformation(statement, statementTransformationSolution)

    def test_20(self):
        """
        Test an attribute assignment of multiple assignments. Which are not changed.
        """
        line = "b = self._VALID_URL.Test"
        statement_solution = "['Assign', 'b = self._VALID_URL.Test', 'b = self._VALID_URL.Test', '=', [['Name', 'b', 'b'], ['Attribute', 'self._VALID_URL.Test', 'self._VALID_URL.Test', None, [['Attribute', 'self._VALID_URL', 'self._VALID_URL', None, [['Name', 'self', 'self']]]]]]]"
        statement = self.check_statement_string(line, statement_solution)
        statementTransformationSolution = "b = self._VALID_URL.Test"
        self.check_exp_transformation(statement, statementTransformationSolution)

    def test_21(self):
        """
        Test an attribute assignment of a assignment in a method.
        """
        line = "mobj = re.match(self._VALID_URL, url)"
        statement_solution = "['Assign', 'mobj = re.match(self._VALID_URL, url)', 'mobj = re.match(self._VALID_URL, url)', '=', [['Name', 'mobj', 'mobj'], ['Call', 're.match(self._VALID_URL, url)', 're.match(self._VALID_URL, url)', 're.match', [['Attribute', 'self._VALID_URL', 'self._VALID_URL', None, [['Name', 'self', 'self']]], ['Name', 'url', 'url']]]]]"
        statement = self.check_statement_string(line, statement_solution)
        statementTransformationSolution = "mobj = re.match(self.EXPTransformation.call(72, 1, False, [['1', 1], ['0', 0]]), EXPTransformation.call(73, 1, False, [['1', 1], ['0', 0]]))"
        self.check_exp_transformation(statement, statementTransformationSolution)

    def test_22(self):
        """
        Test an attribute assignment of a assignment in a method.
        """
        line = "timestamp = parse_iso8601(data['CreatedTime'][:-5])"
        statement_solution = "['Assign', \"timestamp = parse_iso8601(data['CreatedTime'][:-5])\", \"timestamp = parse_iso8601(data['CreatedTime'][:-5])\", '=', [['Name', 'timestamp', 'timestamp'], ['Call', \"parse_iso8601(data['CreatedTime'][:-5])\", \"parse_iso8601(data['CreatedTime'][:-5])\", 'parse_iso8601', [['Subscript', \"data['CreatedTime'][:-5]\", \"data['CreatedTime'][:-5]\", \"data['CreatedTime']\", [['Slice', '-5', '-5', ':', [['UnaryOp', '-5', '-5', 'not', [['USub', '', ''], ['Num', '5', '5']]]]]]]]]]]"
        statement = self.check_statement_string(line, statement_solution)
        statementTransformationSolution = "timestamp = parse_iso8601(data['CreatedTime'][:-5])"
        self.check_exp_transformation(statement, statementTransformationSolution)






if __name__ == '__main__':
    unittest.main()
