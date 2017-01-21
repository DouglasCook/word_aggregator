from collections import Counter, namedtuple

from word_aggregator.spacy_instance import NLP
from word_aggregator import helpers
# TODO remove import once done
from word_aggregator.loader import Loader
from word_aggregator.match import Match


Sentence = namedtuple('Sentence', ['id', 'doc_id', 'tokens'])


class Processor():

    def __init__(self, loader):
        self.sents = []
        self.counter = Counter()
        self.loader = loader

    def process_documents(self):
        docs = self.parse_docs()
        sent_id = 0
        for doc_id, doc in enumerate(docs):
            for sent in doc.sents:
                self.sents.append(Sentence(sent_id, doc_id, sent))
                sent_id += 1
            # TODO use lemma if arg is passed
            self.counter.update(
                [t.lower for t in doc if helpers.is_good_word(t)])

    def parse_docs(self):
        """Return generator of all parsed files from loader."""
        return NLP.pipe(self.loader.read_files())

    def show_me(self, number):
        for matches, count in self.get_most_common(number):
            for m in matches:
                print(m.format_sentence(self.sents))

    def get_most_common(self, number):
        most_common = [(self.build_matches(orth), count)
                       for orth, count in self.counter.most_common(number)]
        return most_common

    def build_matches(self, orth):
        all_matches = []
        for sent in self.sents:
            match_index = [t.i for t in sent.tokens if t.lower == orth]
            if match_index:
                all_matches.append(Match(match_index, sent.id, sent.doc_id))
        return all_matches


if __name__ == '__main__':
    loader = Loader('./docs')
    processor = Processor(loader)
    processor.process_documents()
    boom = processor.show_me(3)
