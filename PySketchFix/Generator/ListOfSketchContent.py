class ListOfSketchContent(object):
    """
    The ListOfSketchContent contains a list of contents for sketches without duplicates and not the original bug file.
    """

    def __init__(self, original_bug_file_content):
        """
        Generate a list of sketch contents which is free from duplicates and not the same as the bug file.

        :param original_bug_file_content: The original bug file content.
        """
        self.contents = []
        self.original_bug_file_content = str(original_bug_file_content)

    def add_content(self, new_content):
        """
        Add a new sketch content to the contents list. Check if the content is already in it or the same as the bug
        file.

        :param new_content: A new content which is added to the list.
        """
        # For every inserted content in the contents of the list. Check if the content is duplicate or the original bug
        # file.
        if not (new_content in self.contents or str(new_content).__eq__(self.original_bug_file_content)):
            self.contents.append(new_content)
