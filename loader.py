import os
import glob

from word_aggregator.spacy_instance import NLP


class Loader():

    def __init__(self, directory):
        self.directory = directory
        self.file_names = []

    def read_files(self):
        file_pattern = os.path.join(self.directory, '*.txt')
        for doc in glob.glob(file_pattern):
            self.file_names.append(doc)
            yield open(doc).read()

    def load_docs(self):
        return NLP.pipe(self.read_files())
