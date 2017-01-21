import os
import glob


class Loader():
    """Class for reading text files from a directory."""

    def __init__(self, directory):
        self.directory = directory
        self.file_paths = []

    def read_files(self):
        """Return generator containing all text files in given directory."""
        file_pattern = os.path.join(self.directory, '*.txt')
        for doc in glob.glob(file_pattern):
            self.file_paths.append(doc)
            yield self.remove_weirdness(open(doc).read())

    def read_indexed_file(self, doc_id):
        """Return contents of document with given id."""
        if doc_id in range(len(self.file_paths)):
            filepath = os.path.join(self.file_paths[doc_id])
        return open(filepath).read()

    @staticmethod
    def remove_weirdness(text):
        """Remove strange comma replacement strings found in doc5 with actual commas."""
        return text.replace(' ? ', ', ')
