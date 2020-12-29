import unittest

from Generator import LineTransformer
from Generator.TransformedLine import ListOfTransformedLines, TransformedLine


class TestTransformedLine(unittest.TestCase):
    """
    Test the TransformedLine.py script in the Generator.TransformedLine.
    """

    def test_is_equal_else(self):
        """
        If you have an else it is replace to an empty string so they will be no transformed line of it.
        """
        code_line = '   else:\n'
        code_line_without_annotations = ''
        line_number = 8
        closer_variables = ['a', 'b']
        closer_variables2 = ['b', 'c']
        transformation = LineTransformer.transform_line(['EXP'], 3, code_line_without_annotations,
                                                        line_number, closer_variables)
        transformed_line = TransformedLine(line_number, code_line,
                                           code_line_without_annotations, transformation)

        # Then make a transformation with closer variables2
        transformation2 = LineTransformer.transform_line(['EXP'], 3,
                                                         code_line_without_annotations, line_number, closer_variables2)
        transformed_line_with_different_transformation = TransformedLine(line_number, code_line,
                                                                         code_line_without_annotations, transformation2)

        transformed_line_with_different_line_number = TransformedLine(1, '    if y < z:\n',
                                                                      'x < y',
                                                                      transformation)
        print("####################################################################################")
        # Here both transformations are the code line again so they are equal.
        print("Transformed Line Original:")
        print("Line: " + str(transformed_line.line_number))
        print("Transformation: " + str(transformed_line.transformation))
        print("Transformed Original Code Line: " + str(transformed_line.transformed_original_code_line))
        print("Code Line: " + str(transformed_line.line))
        print("Code Line w.a.: " + str(transformed_line.line_without_annotations))
        self.assertTrue(transformed_line.is_equal(transformed_line_with_different_transformation))
        print("Transformed Line With diff transformation:")
        print("Line: " + str(transformed_line_with_different_transformation.line_number))
        print("Transformation: " + str(transformed_line_with_different_transformation.transformation))
        print("Transformed Original Code Line: " + str(
            transformed_line_with_different_transformation.transformed_original_code_line))
        print("Code Line: " + str(transformed_line_with_different_transformation.line))
        print("Code Line w.a.: " + str(transformed_line_with_different_transformation.line_without_annotations))
        self.assertFalse(transformed_line.is_equal(transformed_line_with_different_line_number))
        print("Transformed Line With diff line:")
        print("Line: " + str(transformed_line_with_different_line_number.line_number))
        print("Transformation: " + str(transformed_line_with_different_line_number.transformation))
        print("Transformed Original Code Line: " + str(
            transformed_line_with_different_line_number.transformed_original_code_line))
        print("Code Line: " + str(transformed_line_with_different_line_number.line))
        print("Code Line w.a.: " + str(transformed_line_with_different_line_number.line_without_annotations))
        self.assertTrue(transformed_line.is_equal(transformed_line))

    def test_is_equal(self):
        """
        Test the is equal method of the transformed line.
        """
        code_lines = ['def mid(x, y, z):\n', '    m = z\n', '    if y < z:\n', '        if x < y:\n',
                      '            m = y\n', '        elif x < z:\n', '            m = y # m = x\n',
                      '        if x > y:\n', '            m = y\n', '        elif x > z:\n', '            m = x\n',
                      '    return m\n']
        code_lines_without_annotations = ['mid(x, y, z)', 'm = z', 'y < z', 'x < y', 'm = y', 'x < z', 'm = y ',
                                          'x > y', 'm = y', 'x > z', 'm = x', 'return m']

        closer_variables = ['a', 'b']
        closer_variables2 = ['b', 'c']
        for line_number in range(1, len(code_lines)):
            # Make at first a transformation with closer variables 1.
            transformation = LineTransformer.transform_line(['EXP'], 3, code_lines_without_annotations[line_number - 1],
                                                            line_number, closer_variables)
            transformed_line = TransformedLine(line_number, code_lines[line_number - 1],
                                               code_lines_without_annotations[line_number - 1], transformation)

            # Then make a transformation with closer variables2
            transformation2 = LineTransformer.transform_line(['EXP'], 3,
                                                             code_lines_without_annotations[line_number - 1],
                                                             line_number, closer_variables2)
            transformed_line_with_different_transformation = TransformedLine(line_number, code_lines[line_number - 1],
                                                                             code_lines_without_annotations[
                                                                                 line_number - 1], transformation2)

            if line_number != 1:
                transformed_line_with_different_line_number = TransformedLine(1, code_lines[0],
                                                                              code_lines_without_annotations[0],
                                                                              transformation)
            else:
                transformed_line_with_different_line_number = TransformedLine(2, code_lines[1],
                                                                              code_lines_without_annotations[1],
                                                                              transformation)
            print("####################################################################################")
            print("Transformed Line Original:")
            print("Line: " + str(transformed_line.line_number))
            print("Transformation: " + str(transformed_line.transformation))
            print("Transformed Original Code Line: " + str(transformed_line.transformed_original_code_line))
            print("Code Line: " + str(transformed_line.line))
            print("Code Line w.a.: " + str(transformed_line.line_without_annotations))
            self.assertFalse(transformed_line.is_equal(transformed_line_with_different_transformation))
            print("Transformed Line With diff transformation:")
            print("Line: " + str(transformed_line_with_different_transformation.line_number))
            print("Transformation: " + str(transformed_line_with_different_transformation.transformation))
            print("Transformed Original Code Line: " + str(
                transformed_line_with_different_transformation.transformed_original_code_line))
            print("Code Line: " + str(transformed_line_with_different_transformation.line))
            print("Code Line w.a.: " + str(transformed_line_with_different_transformation.line_without_annotations))
            self.assertFalse(transformed_line.is_equal(transformed_line_with_different_line_number))
            print("Transformed Line With diff line:")
            print("Line: " + str(transformed_line_with_different_line_number.line_number))
            print("Transformation: " + str(transformed_line_with_different_line_number.transformation))
            print("Transformed Original Code Line: " + str(
                transformed_line_with_different_line_number.transformed_original_code_line))
            print("Code Line: " + str(transformed_line_with_different_line_number.line))
            print("Code Line w.a.: " + str(transformed_line_with_different_line_number.line_without_annotations))
            self.assertTrue(transformed_line.is_equal(transformed_line))

    def test_transformed_line_7(self):
        """
        Test the transformation of line 7.
        """
        code_line_number = 7
        code_lines = ['def mid(x, y, z):\n', '    m = z\n', '    if y < z:\n', '        if x < y:\n',
                      '            m = y\n', '        elif x < z:\n', '            m = y # m = x\n', '    else:\n',
                      '        if x > y:\n', '            m = y\n', '        elif x > z:\n', '            m = x\n',
                      '    return m\n']
        code_lines_without_annotations = ['mid(x, y, z)', 'm = z', 'y < z', 'x < y', 'm = y', 'x < z', 'm = y ', '',
                                          'x > y', 'm = y', 'x > z', 'm = x', 'return m']
        current_code_line = code_lines[code_line_number - 1]
        current_code_line_without_annotations = code_lines_without_annotations[code_line_number - 1]

        # Make a new list where the transformations are stored to the current line. Here the original code line is in.
        list_of_line_transformations = ListOfTransformedLines(code_line_number, current_code_line,
                                                              current_code_line_without_annotations)
        self.assertEqual(list_of_line_transformations.transformed_lines[0].transformed_original_code_line,
                         current_code_line)
        self.assertEqual(list_of_line_transformations.line_number, code_line_number)
        self.assertEqual(len(list_of_line_transformations.transformed_lines), 1)

        # Make a new transformation to line 7.
        transformed_line7_solution = "            m = EXPTransformation.call(2, 2, False, [['a', a], ['b', b], ['z', z], ['m', m]]) # m = x\n"
        transformation_l7 = "m = EXPTransformation.call(2, 2, False, [['a', a], ['b', b], ['z', z], ['m', m]]) "
        transformed_line7 = TransformedLine(code_line_number, current_code_line,
                                            current_code_line_without_annotations, transformation_l7)
        self.assertEqual(transformed_line7_solution, transformed_line7.transformed_original_code_line)

        list_of_line_transformations.add_transformed_line(transformed_line7)
        list_of_line_transformations.add_transformed_line(transformed_line7)
        self.assertEqual(len(list_of_line_transformations.transformed_lines), 2)
        self.assertEqual(list_of_line_transformations.line_number, code_line_number)
        self.assertEqual(list_of_line_transformations.transformed_lines[0].transformed_original_code_line,
                         current_code_line)
        self.assertEqual(list_of_line_transformations.transformed_lines[1].transformed_original_code_line,
                         transformed_line7_solution)


    def test_transformed_line_6(self):
        """
        Test to add two transformations of line 6 to the list.
        """
        code_line_number = 6
        code_lines = ['def mid(x, y, z):\n', '    m = z\n', '    if y < z:\n', '        if x < y:\n',
                      '            m = y\n', '        elif x < z:\n', '            m = y # m = x\n', '    else:\n',
                      '        if x > y:\n', '            m = y\n', '        elif x > z:\n', '            m = x\n',
                      '    return m\n']
        code_lines_without_annotations = ['mid(x, y, z)', 'm = z', 'y < z', 'x < y', 'm = y', 'x < z', 'm = y ', '',
                                          'x > y', 'm = y', 'x > z', 'm = x', 'return m']
        current_code_line = code_lines[code_line_number - 1]
        current_code_line_without_annotations = code_lines_without_annotations[code_line_number - 1]

        # Make a new list where the transformations are stored to the current line. Here the original code line is in.
        list_of_line_transformations = ListOfTransformedLines(code_line_number, current_code_line,
                                                              current_code_line_without_annotations)
        self.assertEqual(list_of_line_transformations.transformed_lines[0].transformed_original_code_line,
                         current_code_line)
        self.assertEqual(list_of_line_transformations.line_number, code_line_number)
        self.assertEqual(len(list_of_line_transformations.transformed_lines), 1)

        # Make a new transformation to line 6.
        transformed_line6_solution = "        elif (EXPTransformation.call(1, 6, False, [['m', m], ['x', x], ['y', y], ['z', z]]) < " \
                                     "EXPTransformation.call(2, 6, False, [['m', m], ['x', x], ['y', y], ['z', z]])):\n"
        transformation_l6 = "(EXPTransformation.call(1, 6, False, [['m', m], ['x', x], ['y', y], ['z', z]]) < " \
                            "EXPTransformation.call(2, 6, False, [['m', m], ['x', x], ['y', y], ['z', z]]))"
        transformed_line6 = TransformedLine(code_line_number, current_code_line, current_code_line_without_annotations,
                                            transformation_l6)
        self.assertEqual(transformed_line6_solution, transformed_line6.transformed_original_code_line)
        list_of_line_transformations.add_transformed_line(transformed_line6)
        self.assertEqual(list_of_line_transformations.line_number, code_line_number)
        self.assertEqual(len(list_of_line_transformations.transformed_lines), 2)
        self.assertEqual(list_of_line_transformations.transformed_lines[0].transformed_original_code_line,
                         current_code_line)
        self.assertEqual(list_of_line_transformations.transformed_lines[1].transformed_original_code_line,
                         transformed_line6_solution)

        # Make a new transformation to line 6.
        transformed_line6_solution_2 = "        elif COMTransformation.call(1, 6, False, ['x', x], ['z', z]):\n"
        transformation_l6_2 = "COMTransformation.call(1, 6, False, ['x', x], ['z', z])"
        transformed_line6_2 = TransformedLine(code_line_number, current_code_line,
                                              current_code_line_without_annotations,
                                              transformation_l6_2)
        self.assertEqual(transformed_line6_solution_2, transformed_line6_2.transformed_original_code_line)
        list_of_line_transformations.add_transformed_line(transformed_line6_2)
        self.assertEqual(list_of_line_transformations.line_number, code_line_number)
        self.assertEqual(len(list_of_line_transformations.transformed_lines), 3)
        self.assertEqual(list_of_line_transformations.transformed_lines[0].transformed_original_code_line,
                         current_code_line)
        self.assertEqual(list_of_line_transformations.transformed_lines[1].transformed_original_code_line,
                         transformed_line6_solution)
        self.assertEqual(list_of_line_transformations.transformed_lines[2].transformed_original_code_line,
                         transformed_line6_solution_2)


if __name__ == '__main__':
    unittest.main()
