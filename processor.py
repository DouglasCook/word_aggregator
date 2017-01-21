from collections import Counter, namedtuple

from word_aggregator.spacy_instance import NLP
from word_aggregator import helpers
# TODO remove import once done
from word_aggregator.loader import Loader


Sentence = namedtuple('Sentence', ['id', 'doc_id', 'tokens'])


class Match():

    def __init__(self, token_id, token, sent_id):
        # TODO deal with case where there are multiple matches in one sentence
        self.token_id = token_id
        self.token = token
        self.sent_id = sent_id

    def format_(self, sentences):
        sent = sentences[self.sent_id]
        # instead of token can do sent[self.token_id]
        return (sent.tokens, self.token, sent.doc_id)


class Processor():

    def __init__(self):
        self.sents = []
        self.counter = Counter()

    def process_documents(self, docs):
        sent_id = 0
        for doc_id, doc in enumerate(docs):
            for sent in doc.sents:
                self.sents.append(Sentence(sent_id, doc_id, sent))
                sent_id += 1
            # TODO use lemma if arg is passed
            self.counter.update(
                [t.lower for t in doc if helpers.is_good_word(t)])

    def show_me(self, number):
        for matches in self.get_most_common(number):
            print([m.format_(self.sents) for m in matches])

    def get_most_common(self, number):
        most_common = [self.build_matches(orth)
                       for orth, _ in self.counter.most_common(number)]
        return most_common

    def build_matches(self, orth):
        all_matches = []
        for sent in self.sents:
            matches = [Match(i, token, sent.id) for i, token in enumerate(sent.tokens)
                       if token.lower == orth]
            all_matches.extend(matches)
        return all_matches


if __name__ == '__main__':
    loader = Loader('./docs')
    docs = loader.load_docs()

    processor = Processor()
    processor.process_documents(docs)
    boom = processor.show_me(3)
