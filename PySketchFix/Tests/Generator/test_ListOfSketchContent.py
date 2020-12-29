import unittest

from Generator.ListOfSketchContent import ListOfSketchContent


class TestListOfSketchContent(unittest.TestCase):
    """
    Tests the ListOfSketchContent.py script in the Generator.ListOfSketchContent
    """
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

    sketch_file_content1 = \
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

    sketch_file_content2 = \
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

    def test_no_duplicates(self):
        """
        Check if two sketch contents can be applied after each other and are not added twice.
        """
        list_of_sketch_content = ListOfSketchContent(TestListOfSketchContent.bug_file_content)
        list_of_sketch_content.add_content(TestListOfSketchContent.sketch_file_content1)
        list_of_sketch_content.add_content(TestListOfSketchContent.sketch_file_content1)
        self.assertEqual(len(list_of_sketch_content.contents), 1)
        self.assertEqual(list_of_sketch_content.contents[0], TestListOfSketchContent.sketch_file_content1)

        list_of_sketch_content.add_content(TestListOfSketchContent.sketch_file_content2)
        list_of_sketch_content.add_content(TestListOfSketchContent.sketch_file_content2)
        self.assertEqual(len(list_of_sketch_content.contents), 2)
        self.assertEqual(list_of_sketch_content.contents[0], TestListOfSketchContent.sketch_file_content1)
        self.assertEqual(list_of_sketch_content.contents[1], TestListOfSketchContent.sketch_file_content2)

    def test_original_content(self):
        """
        Check if an original bug file content can be applied and is nod added.:
        """
        list_of_sketch_content = ListOfSketchContent(TestListOfSketchContent.bug_file_content)
        list_of_sketch_content.add_content(TestListOfSketchContent.bug_file_content)
        self.assertEqual(len(list_of_sketch_content.contents), 0)
        list_of_sketch_content.add_content(TestListOfSketchContent.sketch_file_content1)
        self.assertEqual(len(list_of_sketch_content.contents), 1)
        self.assertEqual(list_of_sketch_content.contents[0], TestListOfSketchContent.sketch_file_content1)


if __name__ == '__main__':
    unittest.main()
