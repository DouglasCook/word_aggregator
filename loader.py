import os
import glob


class Loader():
    """Class for reading files from directory."""

    def __init__(self, directory):
        self.directory = directory
        self.file_names = []

    def read_files(self):
        """Return generator containing all text files in given directory."""
        file_pattern = os.path.join(self.directory, '*.txt')
        for doc in glob.glob(file_pattern):
            self.file_names.append(doc)
            yield open(doc).read()

    def read_indexed_file(self, doc_id):
        """Return contents of document with given id."""
        if doc_id in range(len(self.file_names)):
            filepath = os.path.join(self.directory, self.file_names[doc_id])
        return open(filepath).read()
