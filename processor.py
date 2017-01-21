from collections import Counter, namedtuple

import word_aggregator.spacy_service as spacy_
from word_aggregator.match import Match
# TODO remove import once done
from word_aggregator.loader import Loader


Sentence = namedtuple('Sentence', ['id', 'doc_id', 'tokens'])


class Processor():

    def __init__(self, loader):
        self.sents = []
        self.counter = Counter()
        self.loader = loader

    def process_documents(self):
        """Build list of sentences in docs and count token occurrences."""
        docs = self.load_parsed_docs()
        sent_id = 0
        for doc_id, doc in enumerate(docs):
            for sent in doc.sents:
                self.sents.append(Sentence(sent_id, doc_id, sent))
                sent_id += 1
            # TODO use lemma if arg is passed
            self.counter.update(
                [t.lower for t in doc if spacy_.is_good_word(t)])

    def get_most_common(self, number):
        most_common = [(orth, count, self.build_matches(orth))
                       for orth, count in self.counter.most_common(number)]
        return most_common

    def build_matches(self, orth):
        """Return a list of sentences containing given word.

        Args:
            orth - int corresponding to a spacy lexeme
        """
        all_matches = []
        for sent in self.sents:
            match_index = [t.i for t in sent.tokens if t.lower == orth]
            if match_index:
                all_matches.append(Match(orth, match_index, sent.id, sent.doc_id))
        return all_matches

    def load_parsed_docs(self):
        """Return parsed versions of all files from loader."""
        return spacy_.parse_docs(self.loader.read_files())

    def display_output(self, number):
        for orth, count, matches in self.get_most_common(number):
            print(f'\n\nFound {count} instances of "{spacy_.convert_to_string(orth)}"')
            for m in matches:
                print(f'\nIn {self.loader.file_names[m.doc_id]}')
                print(m.format_sentence(self.sents))


if __name__ == '__main__':
    LOADER = Loader('./docs')
    PROCESSOR = Processor(LOADER)
    PROCESSOR.process_documents()
    PROCESSOR.display_output(5)
