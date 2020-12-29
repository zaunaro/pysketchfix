import unittest

from Config.ConfigReader import ConfigReader
from Generator.SketchWriter import SketchStore


class TestSketchWriter(unittest.TestCase):
    """
    Tests the SketchWriter.py script in the Generator.SketchWriter
    """

    def test_non_compling_sketch_with_SketchStore(self):
        """
        Test a non compiling sketch to write as a sketch in the sketch writer.
        """
        non_comipling_sketch_content = \
            "from Schemas.ExpressionTransformation import EXPTransformation\n" + \
            "def mid(x, y, z):\n" + \
            "   m = z\n" + \
            "   if y < z:\n" + \
            "       if x < y:\n" + \
            "           m = y\n" + \
            "       elif x < z:\n" + \
            "           m = EXPTransformation.call(2, 7, False, [['m', m], ['x', x], ['y', y], ['z', z]])\n" + \
            "           print(\"Sketch\")\n" + \
            "    else:\n" + \
            "        if x >>>>> y:\n" + \
            "            m = y d\n" + \
            "        elif x > z:\n" + \
            "            m = x\n" + \
            "    return m\n"
        non_compiling_sketch_content = ConfigReader.get_import_statements() + non_comipling_sketch_content

    def test_duplicate_sketch(self):
        """
        Test a a duplicate sketch to write as a sketch in the sketch writer.
        """
        sketch_file_content = \
            "def mid(x, y, z):\n" + \
            "   m = z\n" + \
            "   if y < z:\n" + \
            "       if x < y:\n" + \
            "           m = y\n" + \
            "       elif x < z:\n" + \
            "           m = EXPTransformation.call(2, 7, False, [['m', m], ['x', x], ['y', y], ['z', z]])\n" + \
            "    else:\n" + \
            "        if x > y:\n" + \
            "            m = y\n" + \
            "        elif x > z:\n" + \
            "            m = x\n" + \
            "    return m\n"
        sketch_file_content = ConfigReader.get_import_statements() + sketch_file_content
        self.assertFalse(SketchStore.is_duplicate_content(sketch_file_content))
        self.assertTrue(SketchStore.is_duplicate_content(sketch_file_content))

    def test_bug_file_content(self):
        """
        Test a bug file to write as a sketch in the sketch writer.
        """
        bug_sketch_file_content = \
            "def mid(x, y, z):\n" + \
            "   m = z\n" + \
            "   if y < z:\n" + \
            "       if x < y:\n" + \
            "           m = y\n" + \
            "       elif x < z:\n" + \
            "           m = x" + \
            "    else:\n" + \
            "        if x > y:\n" + \
            "            m = y\n" + \
            "        elif x > z:\n" + \
            "            m = x\n" + \
            "    return m\n"
        bug_sketch_file_content = ConfigReader.get_import_statements() + bug_sketch_file_content
        bug_file_content = \
            "def mid(x, y, z):\n" + \
            "   m = z\n" + \
            "   if y < z:\n" + \
            "       if x < y:\n" + \
            "           m = y\n" + \
            "       elif x < z:\n" + \
            "           m = x" + \
            "    else:\n" + \
            "        if x > y:\n" + \
            "            m = y\n" + \
            "        elif x > z:\n" + \
            "            m = x\n" + \
            "    return m\n"
        bug_file_content = ConfigReader.get_import_statements() + bug_file_content
        self.assertTrue(SketchStore.is_the_same_content_as_bug_file(bug_sketch_file_content, bug_file_content))


if __name__ == '__main__':
    unittest.main()
