from collections import Counter, namedtuple

from word_aggregator.spacy_instance import NLP
from word_aggregator import helpers
# TODO remove import once done
from word_aggregator.loader import Loader


Sentence = namedtuple('Sentence', ['id', 'doc_id', 'tokens'])


class Match():

    highlight_start = '\033[91m' # red
    highlight_end = '\033[0m'

    def __init__(self, token_ids, sent_id, doc_id):
        self.token_ids = token_ids
        self.sent_id = sent_id
        self.doc_id = doc_id

    def format_sentence(self, sentences):
        formatted = [self.format_token(t) for t in sentences[self.sent_id].tokens]
        return ''.join(formatted)

    def format_token(self, token):
        if token.i in self.token_ids:
            return self.make_bold(token.text_with_ws)
        return token.text_with_ws

    def make_bold(self, word):
        return f'{self.highlight_start}{word}{self.highlight_end}'


class Processor():

    def __init__(self):
        self.sents = []
        self.counter = Counter()

    def process_documents(self, docs):
        sent_id = 0
        # TODO can get the doc id from the token - prob don't need doc_id here
        for doc_id, doc in enumerate(docs):
            for sent in doc.sents:
                self.sents.append(Sentence(sent_id, doc_id, sent))
                sent_id += 1
            # TODO use lemma if arg is passed
            self.counter.update(
                [t.lower for t in doc if helpers.is_good_word(t)])

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
    docs = loader.load_docs()

    processor = Processor()
    processor.process_documents(docs)
    boom = processor.show_me(3)
