class Patch(object):
    """
    A patch contains every hole in the code which is reached during a testsuite execution.
    """

    def __init__(self, sketch_name, test_name):
        """
        :param sketch_name: the current sketch which is tested at the moment.
        :param test_name: the current testsuite to which the patch belongs.
        """
        self.test_name = test_name
        self.sketch_name = sketch_name
        self.holes = []

    def add_hole(self, hole_new):
        """
        Adds a hole to the list of holes of the patch. If the hole is already in the patch an error is raised,
        because a patch could only have the hole only one time in the code. This means that after a new execution the
        patches are not reset.

        :param hole_new: The new hole which is inserted.
        :raise RuntimeError: if the hole is already in the array.
        """
        for hole in self.holes:
            if hole.is_equal(hole_new):
                raise RuntimeError("The hole:" + str(hole_new.to_array()) + " could not be inserted because it is "
                                                                            "already in the patch.")
        self.holes.append(hole_new)

    def has_equal_holes(self, other):
        """
        Checks if one patch has the same holes as another patch besides the sketch name and testsuite name.
        This is needed to compare the patches later at the end when the final file for all patches is created.

        :param other: the other patch which self is compared.
        :return: True if they have equal holes, false otherwise.
        """
        if not len(self.holes) == len(other.holes):
            return False
        equal_holes = 0
        for hole in self.holes:
            for otherHole in other.holes:
                if hole.is_equal(otherHole):
                    equal_holes += 1
        if not equal_holes == len(self.holes):
            return False
        return True

    def is_equal(self, other):
        """
        Checks if one patch is equal to another patch. Therefore every hole in the list is checked to ensure that no
        duplicate is in it.

        :param other: the other patch which self is compared.
        :return: True if they are equal, false otherwise.
        """
        if not str.__eq__(self.sketch_name, other.sketch_name):
            return False
        if not str.__eq__(self.test_name, other.test_name):
            return False
        if not len(self.holes) == len(other.holes):
            return False
        return self.has_equal_holes(other)

    def to_array(self):
        """
        :return: The sketch name, testsuite name and the array of holes in one array.
        """
        array = []
        for hole in self.holes:
            array.append(hole.to_array())
        return [self.sketch_name, self.test_name, array]

    def to_patch_format(self):
        """
        :return: A String which is the content of the output file later.
        """
        content = "Sketch: " + str(self.sketch_name) + "\n"
        content += "TestName: " + str(self.test_name) + "\n"
        content += "Holes:" + "\n"
        for hole in self.holes:
            content += str(hole.to_patch_format()) + "\n"
        return content
