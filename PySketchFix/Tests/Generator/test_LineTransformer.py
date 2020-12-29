import unittest

from Generator import LineTransformer


class TestLineTransformer(unittest.TestCase):
    """
    Tests the LineTransformer.py script in the Generator.LineTransformer
    """

    def test_01(self):
        """
        Test the for loop to extract the content.
        """
        line = "	for element in range(2, number):\n"
        formatted_line_solution = "element in range(2, number)"
        removed_line = LineTransformer.remove_code_annotations(line)
        self.assertEqual(formatted_line_solution, removed_line)

    def test_02(self):
        """
        Test the if condition to extract the content.
        """
        line = "		if number % element == 0:\n"
        formatted_line_solution = "number % element == 0"
        removed_line = LineTransformer.remove_code_annotations(line)
        self.assertEqual(formatted_line_solution, removed_line)

    def test_03(self):
        """
        Test the return statement to extract the content.
        """
        line = "		return False:\n"
        formatted_line_solution = "return False"
        removed_line = LineTransformer.remove_code_annotations(line)
        self.assertEqual(formatted_line_solution, removed_line)

    def test_04(self):
        """
        Test the method statement to extract the content.
        """
        line = "def is_prime(number):\n"
        formatted_line_solution = "is_prime(number)"
        removed_line = LineTransformer.remove_code_annotations(line)
        self.assertEqual(formatted_line_solution, removed_line)

    def test_05(self):
        """
        Test the else condition to extract the content.
        """
        line = "                else:\n"
        formatted_line_solution = ""
        removed_line = LineTransformer.remove_code_annotations(line)
        self.assertEqual(formatted_line_solution, removed_line)

    def test_06(self):
        """
        Test the else condition to extract the content.
        """
        line = "            m = y # m = x"
        formatted_line_solution = "m = y"
        removed_line = LineTransformer.remove_code_annotations(line)
        self.assertEqual(formatted_line_solution, removed_line)

    def test_10(self):
        """
        Test the transformation of an assignment.
        """
        print("#######################################")
        transformation_schemas = ['EXP']
        depth = 1
        code_line_without_annotations = "m = z"
        line_number = 2
        closer_variables = ['a', 'b', 'z', 'm']

        transformation = LineTransformer.transform_line(transformation_schemas, depth, code_line_without_annotations,
                                                        line_number, closer_variables)

        transformation_solution = "m = EXPTransformation.call(2, 2, False, [['a', a], ['b', b], ['z', z], ['m', m]])"

        self.assertEqual(transformation_solution, transformation)

        print(code_line_without_annotations)
        print(transformation)

    def test_11(self):
        """
        Test the transformation of a method.
        """
        print("#######################################")
        transformation_schemas = ['EXP']
        depth = 1
        code_line_without_annotations = "is_prime(number)"
        line_number = 2
        closer_variables = ['a', 'b', 'z', 'm']

        transformation = LineTransformer.transform_line(transformation_schemas, depth, code_line_without_annotations,
                                                        line_number, closer_variables)

        transformation_solution = "is_prime(EXPTransformation.call(3, 2, False, [['a', a], ['b', b], ['z', z], ['m', m]]))"

        self.assertEqual(transformation_solution, transformation)

        print(code_line_without_annotations)
        print(transformation)

    def test_12(self):
        """
        Test the transformation of an if condition.
        """
        print("#######################################")
        transformation_schemas = ['COM', 'EXP']
        depth = 1
        code_line_without_annotations = "number == 0 or number == 1"
        line_number = 2
        closer_variables = ['a', 'b', 'z', 'm']

        transformation = LineTransformer.transform_line(transformation_schemas, depth, code_line_without_annotations,
                                                        line_number, closer_variables)

        transformation_solution = "(COMTransformation.call(6, 2, True, EXPTransformation.call(5, 2, True, [['a', a], " \
                                  "['b', b], ['z', z], ['m', m]]), EXPTransformation.call(4, 2, True, [['a', a], " \
                                  "['b', b], ['z', z], ['m', m]])) or COMTransformation.call(9, 2, True, EXPTransform" \
                                  "ation.call(8, 2, True, [['a', a], ['b', b], ['z', z], ['m', m]]), EXPTransformatio" \
                                  "n.call(7, 2, True, [['a', a], ['b', b], ['z', z], ['m', m]])))"

        self.assertEqual(transformation_solution, transformation)

        print(code_line_without_annotations)
        print(transformation)

    def test_13(self):
        """
        Test the transformation of a return function.
        """
        print("#######################################")
        transformation_schemas = ['EXP']
        depth = 1
        code_line_without_annotations = "return False"
        line_number = 2
        closer_variables = ['a', 'b', 'z', 'm']

        transformation = LineTransformer.transform_line(transformation_schemas, depth, code_line_without_annotations,
                                                        line_number, closer_variables)

        transformation_solution = "return EXPTransformation.call(10, 2, False, [['a', a], ['b', b], ['z', z], " \
                                  "['m', m]])"

        self.assertEqual(transformation_solution, transformation)

        print(code_line_without_annotations)
        print(transformation)

    def test_14(self):
        """
        Test the transformation of a for loop.
        """
        print("#######################################")
        transformation_schemas = ['COM']
        depth = 1
        code_line_without_annotations = "element in range(2, number)"
        line_number = 2
        closer_variables = ['a', 'b', 'z', 'm']

        transformation = LineTransformer.transform_line(transformation_schemas, depth, code_line_without_annotations,
                                                        line_number, closer_variables)

        transformation_solution = "COMTransformation.call(11, 2, False, ['element', element], ['range(2, number)', range(2, number)])"

        self.assertEqual(transformation_solution, transformation)

        print(code_line_without_annotations)
        print(transformation)

    def test_15(self):
        """
        Test the transformation of ari and com.
        """
        print("#######################################")
        transformation_schemas = ['ARI', 'COM']
        depth = 1
        code_line_without_annotations = "number % element == 0"
        line_number = 2
        closer_variables = ['a', 'b', 'z', 'm']

        transformation = LineTransformer.transform_line(transformation_schemas, depth, code_line_without_annotations,
                                                        line_number, closer_variables)

        transformation_solution = "COMTransformation.call(13, 2, False, ARITransformation.call(12, 2, True, ['number" \
                                  "', number], ['element', element]), ['0', 0])"

        self.assertEqual(transformation_solution, transformation)

        print(code_line_without_annotations)
        print(transformation)

    def test_16(self):
        """
        Test the transformation of com.
        """
        print("#######################################")
        transformation_schemas = ['COM']
        depth = 1
        code_line_without_annotations = "number % element == 0"
        line_number = 2
        closer_variables = ['a', 'b', 'z', 'm']

        transformation = LineTransformer.transform_line(transformation_schemas, depth, code_line_without_annotations,
                                                        line_number, closer_variables)

        transformation_solution = "COMTransformation.call(14, 2, False, ['(number % element)', (number % element)]," \
                                  " ['0', 0])"

        self.assertEqual(transformation_solution, transformation)

        print(code_line_without_annotations)
        print(transformation)

    def test_17(self):
        """
        Test the transformation of ari.
        """
        print("#######################################")
        transformation_schemas = ['ARI']
        depth = 1
        code_line_without_annotations = "number % element == 0"
        line_number = 2
        closer_variables = ['a', 'b', 'z', 'm']

        transformation = LineTransformer.transform_line(transformation_schemas, depth, code_line_without_annotations,
                                                        line_number, closer_variables)

        transformation_solution = "(ARITransformation.call(15, 2, True, ['number', number], ['element', element]) == 0)"

        self.assertEqual(transformation_solution, transformation)

        print(code_line_without_annotations)
        print(transformation)

    def test_18(self):
        """
        Test the transformation of ari and exp.
        """
        print("#######################################")
        transformation_schemas = ['ARI', 'EXP']
        depth = 1
        code_line_without_annotations = "number % element == 0"
        line_number = 2
        closer_variables = ['a', 'b', 'z', 'm']

        transformation = LineTransformer.transform_line(transformation_schemas, depth, code_line_without_annotations,
                                                        line_number, closer_variables)

        transformation_solution = "(ARITransformation.call(18, 2, True, EXPTransformation.call(17, 2, True, [['a', a]" \
                                  ", ['b', b], ['z', z], ['m', m]]), EXPTransformation.call(16, 2, True, [['a', a], " \
                                  "['b', b], ['z', z], ['m', m]])) == 0)"

        self.assertEqual(transformation_solution, transformation)

        print(code_line_without_annotations)
        print(transformation)

    def test_19(self):
        """
        Test the transformation of exp and com.
        """
        print("#######################################")
        transformation_schemas = ['COM', 'EXP']
        depth = 1
        code_line_without_annotations = "number % element == 0"
        line_number = 2
        closer_variables = ['a', 'b', 'z', 'm']

        transformation = LineTransformer.transform_line(transformation_schemas, depth, code_line_without_annotations,
                                                        line_number, closer_variables)

        transformation_solution = "COMTransformation.call(23, 2, False, ['(number % element)', (number % element)], EXPTransformation.call(22, 2, True, [['a', a], ['b', b], ['z', z], ['m', m]]))"

        self.assertEqual(transformation_solution, transformation)

        print(code_line_without_annotations)
        print(transformation)

    def test_20(self):
        """
        Test the transformation of exp.
        """
        print("#######################################")
        transformation_schemas = ['EXP']
        depth = 1
        code_line_without_annotations = "number % element == 0"
        line_number = 2
        closer_variables = ['a', 'b', 'z', 'm']

        transformation = LineTransformer.transform_line(transformation_schemas, depth, code_line_without_annotations,
                                                        line_number, closer_variables)

        transformation_solution = "((number % element) == EXPTransformation.call(24, 2, False, [['a', a], ['b', b]," \
                                  " ['z', z], ['m', m]]))"

        self.assertEqual(transformation_solution, transformation)

        print(code_line_without_annotations)
        print(transformation)

    def test_21(self):
        """
        Test the transformation of a for loop with exp.
        """
        print("#######################################")
        transformation_schemas = ['EXP']
        depth = 1
        code_line_without_annotations = "element in range(2, number)"
        line_number = 2
        closer_variables = ['a', 'b', 'z', 'm']

        transformation = LineTransformer.transform_line(transformation_schemas, depth, code_line_without_annotations,
                                                        line_number, closer_variables)

        transformation_solution = "(EXPTransformation.call(25, 2, False, [['a', a], ['b', b], ['z', z], ['m', m]]) in range(2, number))"

        self.assertEqual(transformation_solution, transformation)

        print(code_line_without_annotations)
        print(transformation)

    def test_22(self):
        """
        Test the transformation of a for loop with exp and com.
        """
        print("#######################################")
        transformation_schemas = ['EXP', 'COM']
        depth = 1
        code_line_without_annotations = "element in range(2, number)"
        line_number = 2
        closer_variables = ['a', 'b', 'z', 'm']

        transformation = LineTransformer.transform_line(transformation_schemas, depth, code_line_without_annotations,
                                                        line_number, closer_variables)

        transformation_solution = "COMTransformation.call(27, 2, False, EXPTransformation.call(26, 2, True, [['a', a], ['b', b], ['z', z], ['m', m]]), ['range(2, number)', range(2, number)])"

        self.assertEqual(transformation_solution, transformation)

        print(code_line_without_annotations)
        print(transformation)

    def test_23(self):
        """
        Test the transformation of ari, exp and com.
        """
        print("#######################################")
        transformation_schemas = ['ARI', 'COM', 'EXP']
        depth = 1
        code_line_without_annotations = "number % element == 0"
        line_number = 2
        closer_variables = ['a', 'b', 'z', 'm']

        transformation = LineTransformer.transform_line(transformation_schemas, depth, code_line_without_annotations,
                                                        line_number, closer_variables)

        transformation_solution = "COMTransformation.call(32, 2, False, ARITransformation.call(30, 2, True, EXPTransformation.call(29, 2, True, [['a', a], ['b', b], ['z', z], ['m', m]]), EXPTransformation.call(28, 2, True, [['a', a], ['b', b], ['z', z], ['m', m]])), EXPTransformation.call(31, 2, True, [['a', a], ['b', b], ['z', z], ['m', m]]))"

        self.assertEqual(transformation_solution, transformation)

        print(code_line_without_annotations)
        print(transformation)

    def test_24(self):
        """
        Test the transformation of ari.
        """
        print("#######################################")
        transformation_schemas = ['ARI']
        depth = 1
        code_line_without_annotations = "number % element == 0"
        line_number = 2
        closer_variables = ['a', 'b', 'z', 'm']

        transformation = LineTransformer.transform_line(transformation_schemas, depth, code_line_without_annotations,
                                                        line_number, closer_variables)

        transformation_solution = "(ARITransformation.call(33, 2, True, ['number', number], ['element', element]) == 0)"

        self.assertEqual(transformation_solution, transformation)

        print(code_line_without_annotations)
        print(transformation)

    def test_25(self):
        """
        Test the transformation of com.
        """
        print("#######################################")
        transformation_schemas = ['COM']
        depth = 1
        code_line_without_annotations = "number % element == 0"
        line_number = 2
        closer_variables = ['a', 'b', 'z', 'm']

        transformation = LineTransformer.transform_line(transformation_schemas, depth, code_line_without_annotations,
                                                        line_number, closer_variables)

        transformation_solution = "COMTransformation.call(34, 2, False, ['(number % element)', (number % element)]," \
                                  " ['0', 0])"

        self.assertEqual(transformation_solution, transformation)

        print(code_line_without_annotations)
        print(transformation)

    def test_26(self):
        """
        Test the transformation of com.
        """
        print("#######################################")
        transformation_schemas = ['COM']
        depth = 1
        code_line_without_annotations = "number == 0 or number == 1"
        line_number = 2
        closer_variables = ['a', 'b', 'z', 'm']

        transformation = LineTransformer.transform_line(transformation_schemas, depth, code_line_without_annotations,
                                                        line_number, closer_variables)

        transformation_solution = "(COMTransformation.call(35, 2, True, ['number', number], ['0', 0]) or COMTransformation.call(36, 2, True, ['number', number], ['1', 1]))"

        self.assertEqual(transformation_solution, transformation)

        print(code_line_without_annotations)
        print(transformation)

    def test_27(self):
        """
        Test the transformation of com.
        """
        print("#######################################")
        transformation_schemas = ['LOG', 'COM', 'EXP', 'ARI']
        depth = 1
        code_line_without_annotations = "number == 0 or number == 1"
        line_number = 2
        closer_variables = ['a', 'b', 'z', 'm']

        transformation = LineTransformer.transform_line(transformation_schemas, depth, code_line_without_annotations,
                                                        line_number, closer_variables)

        transformation_solution = "LOGTransformation.call(43, 2, False, COMTransformation.call(39, 2, True, " \
                                  "EXPTransformation.call(38, 2, True, [['a', a], ['b', b], ['z', z], ['m', m]]), " \
                                  "EXPTransformation.call(37, 2, True, [['a', a], ['b', b], ['z', z], ['m', m]])), " \
                                  "COMTransformation.call(42, 2, True, EXPTransformation.call(41, 2, True, [['a', a]," \
                                  " ['b', b], ['z', z], ['m', m]]), EXPTransformation.call(40, 2, True, [['a', a], " \
                                  "['b', b], ['z', z], ['m', m]])))"

        self.assertEqual(transformation_solution, transformation)

        print(code_line_without_annotations)
        print(transformation)

    def test_28(self):
        """
        Test the transformation of com.
        """
        print("#######################################")
        transformation_schemas = ['LOG']
        depth = 1
        code_line_without_annotations = "number == 0 or number == 1"
        line_number = 2
        closer_variables = ['a', 'b', 'z', 'm']

        transformation = LineTransformer.transform_line(transformation_schemas, depth, code_line_without_annotations,
                                                        line_number, closer_variables)

        transformation_solution = "LOGTransformation.call(44, 2, False, ['(number == 0)', (number == 0)]," \
                                  " ['(number == 1)', (number == 1)])"

        self.assertEqual(transformation_solution, transformation)

        print(code_line_without_annotations)
        print(transformation)

    def test_29(self):
        """
        Test the transformation of com.
        """
        print("#######################################")
        transformation_schemas = ['LOG', 'EXP']
        depth = 1
        code_line_without_annotations = "number == 0 or number == 1"
        line_number = 2
        closer_variables = ['a', 'b', 'z', 'm']

        transformation = LineTransformer.transform_line(transformation_schemas, depth, code_line_without_annotations,
                                                        line_number, closer_variables)

        transformation_solution = "LOGTransformation.call(49, 2, False, ['(number == 0)', (number == 0)], ['(number" \
                                  " == 1)', (number == 1)])"

        self.assertEqual(transformation_solution, transformation)

        print(code_line_without_annotations)
        print(transformation)

    def test_30(self):
        """
        Test the transformation of com.
        """
        print("#######################################")
        transformation_schemas = ['LOG', 'COM', 'EXP']
        depth = 1
        code_line_without_annotations = "number == 0 or number == 1"
        line_number = 2
        closer_variables = ['a', 'b', 'z', 'm']

        transformation = LineTransformer.transform_line(transformation_schemas, depth, code_line_without_annotations,
                                                        line_number, closer_variables)

        transformation_solution = "LOGTransformation.call(56, 2, False, COMTransformation.call(52, 2, True, " \
                                  "EXPTransformation.call(51, 2, True, [['a', a], ['b', b], ['z', z], ['m', m]]), " \
                                  "EXPTransformation.call(50, 2, True, [['a', a], ['b', b], ['z', z], ['m', m]])), " \
                                  "COMTransformation.call(55, 2, True, EXPTransformation.call(54, 2, True, [['a', a]" \
                                  ", ['b', b], ['z', z], ['m', m]]), EXPTransformation.call(53, 2, True, [['a', a]" \
                                  ", ['b', b], ['z', z], ['m', m]])))"

        self.assertEqual(transformation_solution, transformation)

        print(code_line_without_annotations)
        print(transformation)


if __name__ == '__main__':
    unittest.main()
