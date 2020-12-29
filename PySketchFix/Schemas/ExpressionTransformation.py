import random

from Stores.Hole import Hole
from Stores.PatchStore import PatchStore


class EXPTransformation:
    """
    The EXP Transformation transforms variables and constants and swap it with variables near by. Here the type of the
    transformation are hold, their operators and the current holes in the transformation. This is stored to ensure that
    in one testsuite execution one hole has a concrete value to it and only at the next testsuite execution the value is
    changed. This ensures that the hole value doesn't change if the hole is called once again.
    """
    TYPE = "EXP"
    current_holes = []

    @staticmethod
    def clear_current_holes():
        """
        If the testsuite execution (iteration) is over the current holes are deleted.
        """
        EXPTransformation.current_holes = []

    @staticmethod
    def add_to_current_holes(hole_new):
        """
        A hole is appended to the array. If the hole is already in the array, a value error is raised. This could not be
        possible because in one execution a hole only can be reached one single time.

        :param hole_new: The new hole which is added to the array.
        :raise: RuntimeError: if the hole could not be inserted because it is already in the current holes.
        """
        for hole in EXPTransformation.current_holes:
            if hole.is_equal(hole_new):
                raise RuntimeError(
                    "The hole:" + str(hole_new.to_array()) + " could not be inserted because it is already in the "
                    + EXPTransformation.TYPE + " Transformation.")
        EXPTransformation.current_holes.append(hole_new)

    @staticmethod
    def find_hole(hole_number):
        """
        The current holes array is searched for a specific hole number.

        :param hole_number: The hole number of the hole which is searched in the current holes.
        :return: the hole which is searched and none, if the hole number could not be found.
        """
        for hole in EXPTransformation.current_holes:
            if hole.hole_number == hole_number:
                return hole
        return None

    @staticmethod
    def call(hole_number: int, line_number: int, parent: bool, closer_variables):
        """
        This method is called in the code of the bug file. This is actually the code which is executed instead of the
        original buggy code. At first the current holes is searched for the hole_number. If it is not already in the
        array then the closer variables are fetched from the array. Then a random value of the closer variables are
        chosen and the value is calculated.

        :param hole_number: The number of the hole in the code.
        :param line_number: The line number of the hole.
        :param parent: If the transformation is in another transformation then this value is true.
        :param closer_variables: The closer variables in the lines above or under the statement.
        :return: the value of the call if it has no parent, otherwise an array of the changed code as string and the
        value of it.
        :raise: RuntimeError: if the array of closer variables is empty and if the hole is taken again but the variable
        is not there anymore.
        """
        # Check if the length of the closer variables is filled.
        if len(closer_variables) == 0:
            raise RuntimeError("The closer variables of hole: " + str(hole_number) + " is empty.")

        # First of all is searched, if the hole has already been called, then the variable which has been taken is now
        # taken again.
        value = None
        current_hole = EXPTransformation.find_hole(hole_number)
        if current_hole is not None:
            variable = current_hole.varoperator
            for i in range(len(closer_variables)):
                if variable == closer_variables[i][0]:
                    value = closer_variables[i][1]
                    break
            if value is None:
                raise RuntimeError("The current hole with hole number: " + str(hole_number) + " is not found.")
        else:
            # Choose a random variable of the closer variables.
            random_number = random.randrange(0, len(closer_variables), 1)
            changed_code = [str(closer_variables[random_number][0])]
            value = closer_variables[random_number][1]

            # Create a new current hole and add it to the current holes (if isn't already in it).
            current_hole = Hole(hole_number, line_number, changed_code, EXPTransformation.TYPE, changed_code[0])
            EXPTransformation.add_to_current_holes(current_hole)

            # If the transformation has no parent (then the parent will add the transformation) it is added in the patch
            # store.
            if not parent:
                PatchStore.add_hole_to_patch(current_hole)

        # If it has a parent then an array is returned which code is changed otherwise only the value is returned.
        # This is done because the parent is a transformation as well and has an left and right value array. Here
        # the transformation is represented as changed code and the value of the transformation.
        if not parent:
            return value
        else:
            return [current_hole.array_of_changed_code[0], value]
