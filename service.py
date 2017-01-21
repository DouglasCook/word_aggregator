from collections import Counter, namedtuple

from word_aggregator.spacy_instance import NLP
from word_aggregator import helpers
# TODO remove import once done
from word_aggregator.loader import Loader


Sent = namedtuple('Sent', ['id', 'doc_id', 'sentence'])
Toke = namedtuple('Toke', ['id', 'sent_id'])


class Processor():

    def __init__(self):
        self.sents = []
        self.counter = Counter()

    def process_documents(self, docs):
        for doc_id, doc in enumerate(docs):
            sents = [Sent(i, doc_id, sent) for i, sent in enumerate(doc.sents)]
            self.sents.extend(sents)
            # TODO use lemma if arg is passed
            self.counter.update(
                [t.lower for t in doc if helpers.is_good_word(t)])

    def get_most_common(self, number):
        most_common = [self.build_matches(orth)
                       for orth, _ in self.counter.most_common(number)]
        return most_common

    def build_matches(self, orth):
        all_matches = []
        for sent in self.sents:
            matches = [Toke(i, sent.id) for i, token in enumerate(sent.sentence)
                       if token.lower == orth]
            all_matches.extend(matches)
        return all_matches

    def format_match(self, match):
        sent = self.sents[match.sent_id]
        return (sent.sentence, sent.sentence[match.id], sent.doc_id)


if __name__ == '__main__':
    loader = Loader('./docs')
    docs = loader.load_docs()

    processor = Processor()
    processor.process_documents(docs)
    boom = processor.get_most_common(20)
