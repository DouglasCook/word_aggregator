import os
import glob

from word_aggregator.logger import logger


class TextFileLoader(object):
    """Class for reading text files from a directory."""

    def __init__(self, directory):
        self.directory = directory
        self.file_paths = []

    def read_files(self):
        """Return generator containing all text files in given directory."""
        file_pattern = os.path.join(self.directory, '*.txt')
        for doc in glob.glob(file_pattern):
            logger.info(f'Found file {doc}')
            self.file_paths.append(doc)
            yield self.remove_weirdness(open(doc).read())

    @staticmethod
    def remove_weirdness(text):
        """Remove strange comma replacement strings found in doc5 with actual commas."""
        return text.replace(' ? ', ', ')
