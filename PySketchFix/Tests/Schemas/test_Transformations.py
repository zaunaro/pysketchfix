import unittest

from Schemas.ArithmeticTransformation import ARITransformation
from Schemas.ComparisonTransformation import COMTransformation
from Schemas.ExpressionTransformation import EXPTransformation
from Schemas.LogicalTransformation import LOGTransformation
from Schemas.TransformationManager import TransformationManager
from Stores.PatchStore import PatchStore


class TestTransformations(unittest.TestCase):
    """
    Tests the ARITransformation.py, EXPTransformation.py, COMTransformation.py, TransformationManager.py and
    LOGTransformation.py scripts in the Schemas
    """
    ITERATIONS = 10000

    def test_creating_arithmetic_transformation(self):
        """
        Tests to create an arithmetic transformation and then execute it by call.
        """
        TransformationManager.clear_number_of_transformations()
        TransformationManager.clear_current_holes()
        PatchStore.clear_current_patch()
        PatchStore.set_current_sketch_and_test("sketch1", "test1")
        self.assertEqual(str(TransformationManager.create_transformation("ARI", 1, False, "a", "b")),
                         "ARITransformation.call(1, 1, False, ['a', a], ['b', b])")
        a = 1
        b = 2
        ARITransformation.call(1, 1, False, ['a', a], ['b', b])
        self.assertIsNotNone(ARITransformation.find_hole(1))
        self.assertIsNotNone(PatchStore.current_patch)
        print(PatchStore.current_patch.to_array())
        ARITransformation.call(1, 1, False, ['a', a], ['b', b])
        self.assertTrue(len(PatchStore.current_patch.holes) == 1)

        self.assertEqual(str(TransformationManager.create_transformation("ARI", 2, False, "c", "d")),
                         "ARITransformation.call(2, 2, False, ['c', c], ['d', d])")
        c = 3
        d = 4
        ARITransformation.call(2, 2, False, ['c', c], ['d', d])
        self.assertIsNotNone(ARITransformation.find_hole(2))
        self.assertIsNotNone(PatchStore.current_patch)
        print(PatchStore.current_patch.to_array())
        ARITransformation.call(2, 2, False, ['c', c], ['d', d])
        self.assertTrue(len(PatchStore.current_patch.holes) == 2)

    def test_creating_comparison_transformation(self):
        """
        Tests to create a comparison transformation and then execute it by call.
        """
        TransformationManager.clear_number_of_transformations()
        TransformationManager.clear_current_holes()
        PatchStore.clear_current_patch()
        PatchStore.set_current_sketch_and_test("sketch1", "test1")
        self.assertEqual(str(TransformationManager.create_transformation("COM", 1, False, "a", "b")),
                         "COMTransformation.call(1, 1, False, ['a', a], ['b', b])")
        a = 5
        b = 6
        COMTransformation.call(1, 1, False, ['a', a], ['b', b])
        self.assertIsNotNone(COMTransformation.find_hole(1))
        self.assertIsNotNone(PatchStore.current_patch)
        print(PatchStore.current_patch.to_array())
        COMTransformation.call(1, 1, False, ['a', a], ['b', b])
        self.assertTrue(len(PatchStore.current_patch.holes) == 1)

        self.assertEqual(str(TransformationManager.create_transformation("COM", 2, False, "c", "d")),
                         "COMTransformation.call(2, 2, False, ['c', c], ['d', d])")
        c = 3
        d = 4
        COMTransformation.call(2, 2, False, ['c', c], ['d', d])
        self.assertIsNotNone(COMTransformation.find_hole(2))
        self.assertIsNotNone(PatchStore.current_patch)
        print(PatchStore.current_patch.to_array())
        COMTransformation.call(2, 2, False, ['c', c], ['d', d])
        self.assertTrue(len(PatchStore.current_patch.holes) == 2)

    def test_creating_logical_transformation(self):
        """
        Tests to create a logical transformation and then execute it by call.
        """
        TransformationManager.clear_number_of_transformations()
        TransformationManager.clear_current_holes()
        PatchStore.clear_current_patch()
        PatchStore.set_current_sketch_and_test("sketch1", "test1")
        self.assertEqual(str(TransformationManager.create_transformation("LOG", 1, False, "a", "b")),
                         "LOGTransformation.call(1, 1, False, ['a', a], ['b', b])")
        a = True
        b = False
        LOGTransformation.call(1, 1, False, ['a', a], ['b', b])
        self.assertIsNotNone(LOGTransformation.find_hole(1))
        self.assertIsNotNone(PatchStore.current_patch)
        print(PatchStore.current_patch.to_array())
        LOGTransformation.call(1, 1, False, ['a', a], ['b', b])
        self.assertTrue(len(PatchStore.current_patch.holes) == 1)

        self.assertEqual(str(TransformationManager.create_transformation("LOG", 2, False, "c", "d")),
                         "LOGTransformation.call(2, 2, False, ['c', c], ['d', d])")
        c = True
        d = False
        LOGTransformation.call(2, 2, False, ['c', c], ['d', d])
        self.assertIsNotNone(LOGTransformation.find_hole(2))
        self.assertIsNotNone(PatchStore.current_patch)
        print(PatchStore.current_patch.to_array())
        LOGTransformation.call(2, 2, False, ['c', c], ['d', d])
        self.assertTrue(len(PatchStore.current_patch.holes) == 2)

    def test_creating_expression_transformation(self):
        """
        Tests to create an expression transformation and then execute it by call.
        """
        TransformationManager.clear_number_of_transformations()
        TransformationManager.clear_current_holes()
        PatchStore.clear_current_patch()
        PatchStore.set_current_sketch_and_test("sketch1", "test1")
        has_error = False
        try:
            TransformationManager.create_transformation("EXP", 1, False, "a", "b")
        except RuntimeError:
            has_error = True
        self.assertTrue(has_error)

        self.assertEqual(str(TransformationManager.create_EXP_transformation(1, False, ["a", "b"])),
                         "EXPTransformation.call(1, 1, False, [['a', a], ['b', b]])")
        a = True
        b = False
        EXPTransformation.call(1, 1, False, [['a', a], ['b', b]])
        self.assertIsNotNone(EXPTransformation.find_hole(1))
        self.assertIsNotNone(PatchStore.current_patch)
        print(PatchStore.current_patch.to_array())
        EXPTransformation.call(1, 1, False, [['a', a], ['b', b]])
        self.assertTrue(len(PatchStore.current_patch.holes) == 1)

        self.assertEqual(str(TransformationManager.create_EXP_transformation(2, False, ["c", "d"])),
                         "EXPTransformation.call(2, 2, False, [['c', c], ['d', d]])")
        c = True
        d = False
        EXPTransformation.call(2, 2, False, [['c', c], ['d', d]])
        self.assertIsNotNone(EXPTransformation.find_hole(2))
        self.assertIsNotNone(PatchStore.current_patch)
        print(PatchStore.current_patch.to_array())
        EXPTransformation.call(2, 2, False, [['c', c], ['d', d]])
        self.assertTrue(len(PatchStore.current_patch.holes) == 2)

    def test_creating_comparison_expression_transformation(self):
        """
        Tests the combination of comparison and expression transformation. Therefore COM transformation is created,
        containing on the left and right side an comparison transformation. After creating the transformation, the
        hole is called multiple times.
        """
        TransformationManager.clear_number_of_transformations()
        TransformationManager.clear_current_holes()
        PatchStore.clear_current_patch()
        PatchStore.set_current_sketch_and_test("sketch1", "test1")
        a = 1
        b = 2
        transformation = str(TransformationManager.create_transformation("COM", 10, False,
                                                                         "EXPTransformation."
                                                                         "call(2, 10, True, [['a', a], ['b', b]])",
                                                                         "EXPTransformation."
                                                                         "call(3, 10, True, [['a', a], ['b', b]])"))
        self.assertEqual("COMTransformation.call(1, 10, False, "
                         "EXPTransformation.call(2, 10, True, [['a', a], ['b', b]]), "
                         "EXPTransformation.call(3, 10, True, [['a', a], ['b', b]]))", transformation)
        i = 0
        while i < TestTransformations.ITERATIONS:
            COMTransformation.call(1, 10, False, EXPTransformation.call(2, 10, True, [['a', a], ['b', b]]),
                                   EXPTransformation.call(3, 10, True, [['a', a], ['b', b]]))
            i += 1

    def test_creating_arithmetic_expression_transformation(self):
        """
        Tests the combination of arithmetic and expression transformation. Therefore ARI transformation is created,
        containing on the left and right side an expression transformation. After creating the transformation, the
        hole is called multiple times.
        """
        TransformationManager.clear_number_of_transformations()
        TransformationManager.clear_current_holes()
        PatchStore.clear_current_patch()
        PatchStore.set_current_sketch_and_test("sketch1", "test1")
        a = 1
        b = 2
        transformation = str(TransformationManager.create_transformation("ARI", 10, False,
                                                                         "EXPTransformation."
                                                                         "call(2, 10, True, [['a', a], ['b', b]])",
                                                                         "EXPTransformation."
                                                                         "call(3, 10, True, [['a', a], ['b', b]])"))
        self.assertEqual(
            "ARITransformation.call(1, 10, False, EXPTransformation.call(2, 10, True, [['a', a], ['b', b]])"
            ", EXPTransformation.call(3, 10, True, [['a', a], ['b', b]]))", transformation)
        i = 0
        while i < TestTransformations.ITERATIONS:
            ARITransformation.call(1, 10, False, EXPTransformation.call(2, 10, True, [['a', a], ['b', b]]),
                                   EXPTransformation.call(3, 10, True, [['a', a], ['b', b]]))
            i += 1

    def test_creating_logical_expression_transformation(self):
        """
        Tests the combination of expression and logical transformation. Therefore LOG transformation is created,
        containing on the left and right side an expression transformation. After creating the transformation, the
        hole is called multiple times.
        """
        TransformationManager.clear_number_of_transformations()
        TransformationManager.clear_current_holes()
        PatchStore.clear_current_patch()
        PatchStore.set_current_sketch_and_test("sketch1", "test1")
        a = True
        b = False
        transformation = str(TransformationManager.create_transformation("LOG", 10, False,
                                                                         "EXPTransformation."
                                                                         "call(2, 10, True, [['a', a], ['b', b]])",
                                                                         "EXPTransformation."
                                                                         "call(3, 10, True, [['a', a], ['b', b]])"))
        self.assertEqual(
            "LOGTransformation.call(1, 10, False, EXPTransformation.call(2, 10, True, [['a', a], ['b', b]])"
            ", EXPTransformation.call(3, 10, True, [['a', a], ['b', b]]))", transformation)
        i = 0
        while i < TestTransformations.ITERATIONS:
            LOGTransformation.call(1, 10, False, EXPTransformation.call(2, 10, True, [['a', a], ['b', b]]),
                                   EXPTransformation.call(3, 10, True, [['a', a], ['b', b]]))
            i += 1

    def test_creating_logical_comparison_transformation(self):
        """
        Tests the combination of comparison and logical transformation. Therefore LOG transformation is created,
        containing on the left and right side an comparison transformation. After creating the transformation, the
        hole is called multiple times.
        """
        TransformationManager.clear_number_of_transformations()
        TransformationManager.clear_current_holes()
        PatchStore.clear_current_patch()
        PatchStore.set_current_sketch_and_test("sketch1", "test1")
        a = 1
        b = 2
        transformation = str(TransformationManager.create_transformation("LOG", 10, False,
                                                                         "COMTransformation."
                                                                         "call(2, 10, True, ['a', a], ['b', b])",
                                                                         "COMTransformation."
                                                                         "call(3, 10, True, ['a', a], ['b', b])"))
        self.assertEqual(
            "LOGTransformation.call(1, 10, False, COMTransformation.call(2, 10, True, ['a', a], ['b', b]), "
            "COMTransformation.call(3, 10, True, ['a', a], ['b', b]))", transformation)
        i = 0
        while i < TestTransformations.ITERATIONS:
            LOGTransformation.call(1, 10, False, COMTransformation.call(2, 10, True, ['a', a], ['b', b]),
                                   COMTransformation.call(3, 10, True, ['a', a], ['b', b]))
            i += 1

    def test_creating_comparison_arithmetic_transformation(self):
        """
        Tests the combination of comparison and arithmetic transformation. Therefore COM transformation is created,
        containing on the left and right side an arithmetic transformation. After creating the transformation, the
        hole is called multiple times.
        """
        TransformationManager.clear_number_of_transformations()
        TransformationManager.clear_current_holes()
        PatchStore.clear_current_patch()
        PatchStore.set_current_sketch_and_test("sketch1", "test1")
        a = 1
        b = 2
        transformation = str(TransformationManager.create_transformation("COM", 10, False,
                                                                         "ARITransformation."
                                                                         "call(2, 10, True, ['a', a], ['b', b])",
                                                                         "ARITransformation."
                                                                         "call(3, 10, True, ['a', a], ['b', b])"))
        self.assertEqual(
            "COMTransformation.call(1, 10, False, ARITransformation.call(2, 10, True, ['a', a], ['b', b]), "
            "ARITransformation.call(3, 10, True, ['a', a], ['b', b]))", transformation)
        i = 0
        while i < TestTransformations.ITERATIONS:
            COMTransformation.call(1, 10, False, ARITransformation.call(2, 10, True, ['a', a], ['b', b]),
                                   ARITransformation.call(3, 10, True, ['a', a], ['b', b]))
            i += 1

    def test_creating_logical_comparison_expression_transformation(self):
        """
        Tests the combination of logical, comparison and expression transformation. Therefore a LOG transformation is
        created, where on the left and right side is a comparison transformation containing expression transformations.
        After creating the transformation, the hole is called multiple times.
        """
        TransformationManager.clear_number_of_transformations()
        TransformationManager.clear_current_holes()
        PatchStore.clear_current_patch()
        PatchStore.set_current_sketch_and_test("sketch1", "test1")
        a = 1
        b = 2
        transformation = str(TransformationManager.create_transformation("LOG", 10, False,
                                                                         "COMTransformation."
                                                                         "call(2, 10, True, "
                                                                         "EXPTransformation."
                                                                         "call(3, 10, True, [['a', a], ['b', b]]), "
                                                                         "EXPTransformation."
                                                                         "call(4, 10, True, [['a', a], ['b', b]]))",
                                                                         "COMTransformation."
                                                                         "call(5, 10, True, "
                                                                         "EXPTransformation."
                                                                         "call(6, 10, True, [['a', a], ['b', b]]), "
                                                                         "EXPTransformation."
                                                                         "call(7, 10, True, [['a', a], ['b', b]]))"
                                                                         ))
        self.assertEqual(
            "LOGTransformation.call(1, 10, False, "
            "COMTransformation.call(2, 10, True, "
            "EXPTransformation.call(3, 10, True, [['a', a], ['b', b]]), "
            "EXPTransformation.call(4, 10, True, [['a', a], ['b', b]])), "
            "COMTransformation.call(5, 10, True, "
            "EXPTransformation.call(6, 10, True, [['a', a], ['b', b]]), "
            "EXPTransformation.call(7, 10, True, [['a', a], ['b', b]])))", transformation)
        i = 0
        a = 1
        b = 2
        while i < TestTransformations.ITERATIONS:
            ARITransformation.call(1, 10, False,
                                   COMTransformation.call(2, 10, True,
                                                          EXPTransformation.call(3, 10, True, [['a', a], ['b', b]]),
                                                          EXPTransformation.call(4, 10, True, [['a', a], ['b', b]])),
                                   COMTransformation.call(5, 10, True,
                                                          EXPTransformation.call(6, 10, True, [['a', a], ['b', b]]),
                                                          EXPTransformation.call(7, 10, True, [['a', a], ['b', b]])))
            i += 1

    def test_creating_comparison_arithmetic_expression_transformation(self):
        """
        Tests the combination of comparison, arithmetic and expression transformation. Therefore a COM transformation is
        created, where on the left and right side is an arithmetic transformation containing expression transformations.
        After creating the transformation, the hole is called multiple times.
        """
        TransformationManager.clear_number_of_transformations()
        TransformationManager.clear_current_holes()
        PatchStore.clear_current_patch()
        PatchStore.set_current_sketch_and_test("sketch1", "test1")
        a = 1
        b = 2
        transformation = str(TransformationManager.create_transformation("COM", 10, False,
                                                                         "ARITransformation."
                                                                         "call(2, 10, True, "
                                                                         "EXPTransformation."
                                                                         "call(3, 10, True, [['a', a], ['b', b]]), "
                                                                         "EXPTransformation."
                                                                         "call(4, 10, True, [['a', a], ['b', b]]))",
                                                                         "ARITransformation."
                                                                         "call(5, 10, True, "
                                                                         "EXPTransformation."
                                                                         "call(6, 10, True, [['a', a], ['b', b]]), "
                                                                         "EXPTransformation."
                                                                         "call(7, 10, True, [['a', a], ['b', b]]))"
                                                                         ))
        self.assertEqual(
            "COMTransformation.call(1, 10, False, "
            "ARITransformation.call(2, 10, True, "
            "EXPTransformation.call(3, 10, True, [['a', a], ['b', b]]), "
            "EXPTransformation.call(4, 10, True, [['a', a], ['b', b]])), "
            "ARITransformation.call(5, 10, True, "
            "EXPTransformation.call(6, 10, True, [['a', a], ['b', b]]), "
            "EXPTransformation.call(7, 10, True, [['a', a], ['b', b]])))", transformation)
        i = 0
        while i < TestTransformations.ITERATIONS:
            COMTransformation.call(1, 10, False,
                                   ARITransformation.call(2, 10, True,
                                                          EXPTransformation.call(3, 10, True, [['a', a], ['b', b]]),
                                                          EXPTransformation.call(4, 10, True, [['a', a], ['b', b]])),
                                   ARITransformation.call(5, 10, True,
                                                          EXPTransformation.call(6, 10, True, [['a', a], ['b', b]]),
                                                          EXPTransformation.call(7, 10, True, [['a', a], ['b', b]])))
            i += 1

    def test_creating_logical_comparison_arithmetic_expression_transformation(self):
        """
        Tests the combination of comparison, arithmetic and expression transformation. Therefore a COM transformation is
        created, where on the left and right side is an arithmetic transformation containing expression transformations.
        After creating the transformation, the hole is called multiple times.
        """
        TransformationManager.clear_number_of_transformations()
        TransformationManager.clear_current_holes()
        PatchStore.clear_current_patch()
        PatchStore.set_current_sketch_and_test("sketch1", "test1")
        a = 1
        b = 2
        transformation = str(TransformationManager.create_transformation("LOG", 10, False,
                                                                         "COMTransformation."
                                                                         "call(2, 10, True, "
                                                                         "ARITransformation."
                                                                         "call(3, 10, True, "
                                                                         "EXPTransformation."
                                                                         "call(4, 10, True, [['a', a], ['b', b]]), "
                                                                         "EXPTransformation."
                                                                         "call(5, 10, True, [['a', a], ['b', b]])), "
                                                                         "ARITransformation."
                                                                         "call(6, 10, True, "
                                                                         "EXPTransformation."
                                                                         "call(7, 10, True, [['a', a], ['b', b]]), "
                                                                         "EXPTransformation."
                                                                         "call(8, 10, True, [['a', a], ['b', b]])))"
                                                                         ,
                                                                         "COMTransformation."
                                                                         "call(9, 10, True, "
                                                                         "ARITransformation."
                                                                         "call(10, 10, True, "
                                                                         "EXPTransformation."
                                                                         "call(11, 10, True, [['a', a], ['b', b]]), "
                                                                         "EXPTransformation."
                                                                         "call(12, 10, True, [['a', a], ['b', b]])), "
                                                                         "ARITransformation."
                                                                         "call(13, 10, True, "
                                                                         "EXPTransformation."
                                                                         "call(14, 10, True, [['a', a], ['b', b]]), "
                                                                         "EXPTransformation."
                                                                         "call(15, 10, True, [['a', a], ['b', b]])))"
                                                                         ))
        self.assertEqual(
            "LOGTransformation.call(1, 10, False, "
            "COMTransformation.call(2, 10, True, "
            "ARITransformation.call(3, 10, True, "
            "EXPTransformation.call(4, 10, True, [['a', a], ['b', b]]), "
            "EXPTransformation.call(5, 10, True, [['a', a], ['b', b]])), "
            "ARITransformation.call(6, 10, True, "
            "EXPTransformation.call(7, 10, True, [['a', a], ['b', b]]), "
            "EXPTransformation.call(8, 10, True, [['a', a], ['b', b]]))), "
            "COMTransformation.call(9, 10, True, "
            "ARITransformation.call(10, 10, True, "
            "EXPTransformation.call(11, 10, True, [['a', a], ['b', b]]), "
            "EXPTransformation.call(12, 10, True, [['a', a], ['b', b]])), "
            "ARITransformation.call(13, 10, True, "
            "EXPTransformation.call(14, 10, True, [['a', a], ['b', b]]), "
            "EXPTransformation.call(15, 10, True, [['a', a], ['b', b]]))))",
            transformation)
        i = 0
        while i < TestTransformations.ITERATIONS:
            LOGTransformation.call(1, 10, False,
                                   COMTransformation.call(2, 10, True,
                                                          ARITransformation.call(3, 10, True,
                                                                                 EXPTransformation.
                                                                                 call(4, 10, True,
                                                                                      [['a', a], ['b', b]]),
                                                                                 EXPTransformation.
                                                                                 call(5, 10, True,
                                                                                      [['a', a], ['b', b]])),
                                                          ARITransformation.call(6, 10, True,
                                                                                 EXPTransformation.
                                                                                 call(7, 10, True,
                                                                                      [['a', a], ['b', b]]),
                                                                                 EXPTransformation.
                                                                                 call(8, 10, True,
                                                                                      [['a', a], ['b', b]]))),
                                   COMTransformation.call(9, 10, True,
                                                          ARITransformation.call(10, 10, True,
                                                                                 EXPTransformation.
                                                                                 call(11, 10, True,
                                                                                      [['a', a], ['b', b]]),
                                                                                 EXPTransformation.
                                                                                 call(12, 10, True,
                                                                                      [['a', a], ['b', b]])),
                                                          ARITransformation.call(13, 10, True,
                                                                                 EXPTransformation.
                                                                                 call(14, 10, True,
                                                                                      [['a', a], ['b', b]]),
                                                                                 EXPTransformation.
                                                                                 call(15, 10, True,
                                                                                      [['a', a], ['b', b]]))))
            i += 1

    if __name__ == '__main__':
        unittest.main()
