import unittest

from Generator import CloserVariablesFinder


class TestCloserVariablesFinder(unittest.TestCase):
    """
    Tests the CloserVariablesFinder.py script in the Generator.CloserVariablesFinder
    """

    def test_01(self):
        """
        Test the  closer lines. Therefore check line 1 and add 1 as area.
        """
        print("+++ Test 1 +++")
        code_lines_without_annotations = ['mid(x, y, z)', 'm = z', 'y < z', 'x < y', 'm = y', 'x < z', 'm = y # m = x',
                                          'else', 'x > y', 'm = y', 'x > z', 'm = x', 'return m']
        closer_variables = CloserVariablesFinder.get_closer_variables(1, code_lines_without_annotations, 1)
        closer_variables_str = str(closer_variables)
        print(closer_variables_str)
        closer_variables_str_solution = "['m', 'x', 'y', 'z']"
        self.assertEqual(closer_variables_str_solution, closer_variables_str)

    def test_02(self):
        """
        Test the  closer lines. Therefore check line 1 and add 2 as area (def).
        """
        print("+++ Test 2 +++")
        code_lines_without_annotations = ['mid(x, y, z)', 'm = z', 'y < z', 'x < y', 'm = y', 'x < z', 'm = y # m = x',
                                          'else', 'x > y', 'm = y', 'x > z', 'm = x', 'return m']
        closer_variables = CloserVariablesFinder.get_closer_variables(1, code_lines_without_annotations, 2)
        closer_variables_str = str(closer_variables)
        print(closer_variables_str)
        closer_variables_str_solution = "['m', 'x', 'y', 'z']"
        self.assertEqual(closer_variables_str_solution, closer_variables_str)

    def test_03(self):
        """
        Test the  closer lines. Therefore check a line where an expression transformation is located.
        """
        print("+++ Test 3 +++")
        code_lines_without_annotations = ['mid(x, y, z)',
                                          "m = EXPTransformation.call(2, 7, False, [['m', m], ['z', z])",
                                          'y < z', 'x < y', 'm = y', 'x < z', 'm = y # m = x',
                                          'else', 'x > y', 'm = y', 'x > z', 'm = x', 'return m']
        closer_variables = CloserVariablesFinder.get_closer_variables(2, code_lines_without_annotations, 0)
        closer_variables_str = str(closer_variables)
        print(closer_variables_str)
        closer_variables_str_solution = "[]"
        self.assertEqual(closer_variables_str_solution, closer_variables_str)

    def test_04(self):
        """
        Test the  closer lines. Therefore check line 5 and add 0 as area.
        """
        print("+++ Test 4 +++")
        code_lines_without_annotations = ['mid(x, y, z)', 'm = z', 'y < z', 'x < y', 'm = y', 'x < z', 'm = y # m = x',
                                          'else', 'x > y', 'm = y', 'x > z', 'm = x', 'return m']
        closer_variables = CloserVariablesFinder.get_closer_variables(5, code_lines_without_annotations, 0)
        closer_variables_str = str(closer_variables)
        print(closer_variables_str)
        closer_variables_str_solution = "['m', 'y']"
        self.assertEqual(closer_variables_str_solution, closer_variables_str)

    def test_05(self):
        """
        Test the  closer lines. Therefore check line 13 and add 0 as area (return).
        """
        print("+++ Test 5 +++")
        code_lines_without_annotations = ['mid(x, y, z)', 'm = z', 'y < z', 'x < y', 'm = y', 'x < z', 'm = y # m = x',
                                          'else', 'x > y', 'm = y', 'x > z', 'm = x', 'return m']
        closer_variables = CloserVariablesFinder.get_closer_variables(13, code_lines_without_annotations, 0)
        closer_variables_str = str(closer_variables)
        print(closer_variables_str)
        closer_variables_str_solution = "['m']"
        self.assertEqual(closer_variables_str_solution, closer_variables_str)


if __name__ == '__main__':
    unittest.main()
