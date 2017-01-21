import os
import glob
from collections import Counter

from word_aggregator.spacy_instance import NLP
from word_aggregator import helpers


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


class Processor():

    def __init__(self):
        self.sents = []
        self.counter = Counter()

    def process_documents(self, docs):
        for doc in docs:
            self.sents.extend(doc.sents)
            # TODO use lemma if arg is passed
            self.counter.update(
                [t.lower for t in doc if helpers.is_good_word(t)])

    def get_most_common(self, number):
        return [helpers.convert_to_string(t[0])
                for t in self.counter.most_common(number)]


if __name__ == '__main__':
    loader = Loader('./docs')
    docs = loader.load_docs()

    processor = Processor()
    processor.process_documents(docs)
    boom = processor.get_most_common(20)
    import ipdb; ipdb.set_trace()
