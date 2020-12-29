import os

from Config import FileHandler
from Config.ConfigReader import ConfigReader


def write_sketch(sketch_file_content):
    """
    Make a new sketch file with the lines.

    :param sketch_file_content: The content for the new sketch with transformed lines in it as String.
    :return: False, if the sketch could not be created, True if creation was successful.
    """

    # First of all the content is compared with already created sketches and also with the original bug file. Therefore
    # the import statements had to be added.
    sketch_file_content = ConfigReader.get_import_statements() + sketch_file_content
    if not SketchStore.is_valid_content(sketch_file_content):
        return False

    # Then the concrete file name of the sketch is created and the number of sketches is incremented.
    SketchStore.number_of_created_sketches += 1
    sketch_name = ConfigReader.get_bug_file_name() + '_sketch' + str(SketchStore.number_of_created_sketches)
    SKETCH_DIRECTORY = ConfigReader.get_sketch_directory()
    sketch_file = os.path.join(SKETCH_DIRECTORY, sketch_name + '.py')

    # Open the sketch file and write the content.
    file = open(sketch_file, 'w+')
    file.write(sketch_file_content)
    file.close()
    if ConfigReader.get_debug_mode():
        print('✓ Created a new sketch file in: ' + sketch_file)
    return True


def print_statistics(suspicious_lines_without_transformation):
    """
    Prints the number of created sketches, after all sketches are generated in the Generator.

    :param: suspicious_lines_without_transformation The sus lines where no transformation could be found.
    """
    txt = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    txt = txt + "\nx Lines where no transformation is found:" + str(suspicious_lines_without_transformation)
    txt = txt + "\n✓ Number of created sketches:" + str(SketchStore.number_of_created_sketches)
    print(txt)


class SketchStore:
    """
    Here the list of created sketch content is stored and the number of sketches created.
    """
    number_of_created_sketches = 0
    list_of_created_sketch_content = []

    @staticmethod
    def is_valid_content(sketch_file_content):
        """
        Check the content of the sketch. Therefore it is checked, if it isn't a duplicate content and if it is not the
        same as the bug file content. Therefore the import statements are added to the bug file content.

        :param sketch_file_content: The created content for a new sketch file as String.
        :return: True, if the content is valid, False if not.
        """
        bug_file_content = FileHandler.parse_file_for_content_as_string(ConfigReader.get_bug_file())
        bug_file_content = ConfigReader.get_import_statements() + bug_file_content
        if SketchStore.is_the_same_content_as_bug_file(sketch_file_content, bug_file_content):
            return False
        if SketchStore.is_duplicate_content(sketch_file_content):
            return False
        return True

    @staticmethod
    def is_the_same_content_as_bug_file(sketch_file_content, bug_file_content):
        """
        It is checked if the bug file content is the same as the sketch file content. For this the import statements
        has to be added to the bug file as well to compare.

        :param sketch_file_content: The created content for a new sketch file as String.
        :param bug_file_content: The content of the current bug file.
        :return: True, if the content does exists, false if the content is new.
        """
        return str.__eq__(sketch_file_content, bug_file_content)

    @staticmethod
    def is_duplicate_content(sketch_file_content):
        """
        Compare the created content for a new sketch with already created sketches. If it is already created then
        this sketch is skipped. If the content is not created add it into the list.

        :param sketch_file_content: The created content for a new sketch file as String.
        :return: True, if the content does exists, false if the content is new.
        """
        # If the list of created sketches is zero, then no sketch was created before and the new sketch is inserted.
        if len(SketchStore.list_of_created_sketch_content) == 0:
            SketchStore.list_of_created_sketch_content.append(sketch_file_content)
            return False

        # Otherwise it is checked for every member of the sketch list, weather it is equal to the new sketch or not.
        for created_sketch in SketchStore.list_of_created_sketch_content:
            if str.__eq__(created_sketch, sketch_file_content):
                return True
        SketchStore.list_of_created_sketch_content.append(sketch_file_content)
        return False
