from collections import Counter, namedtuple

import word_aggregator.spacy_service as spacy_
from word_aggregator.match import Match


Sentence = namedtuple('Sentence', ['id', 'doc_id', 'tokens'])


class Processor():
    """Class for processing documents and extracting most commonly occurring words."""

    def __init__(self, loader, lemmatise=False):
        """Constructor

        Args:
            loader: loader instance with read_files method
            lemmatise: bool flag for lemmatising tokens instead of lowering
        """
        self.sents = []
        self.counter = Counter()
        self.loader = loader
        self.lemmatise = lemmatise

    def process_documents(self):
        """Build list of sentences in docs and count token occurrences."""
        docs = self.load_parsed_docs()
        sent_id = 0
        for doc_id, doc in enumerate(docs):
            for sent in doc.sents:
                self.sents.append(Sentence(sent_id, doc_id, sent))
                sent_id += 1
            self.counter.update(
                [self.normalise_token(t) for t in doc if spacy_.is_good_word(t)])

    def get_most_common(self, number):
        """Return list containing matches for given number of most commonly
        occurring words."""
        most_common = [(orth, count, self.build_matches(orth))
                       for orth, count in self.counter.most_common(number)]
        self.print_summary(most_common)
        return most_common

    def build_matches(self, orth):
        """Return a list of sentences containing given word."""
        all_matches = []
        for sent in self.sents:
            match_index = [t.i for t in sent.tokens if self.normalise_token(t) == orth]
            if match_index:
                all_matches.append(Match(orth, match_index, sent.id, sent.doc_id))
        return all_matches

    def load_parsed_docs(self):
        """Return parsed versions of all files from loader."""
        return spacy_.parse_docs(self.loader.read_files())

    def normalise_token(self, token):
        """Normalise given token."""
        if self.lemmatise:
            return token.lemma
        return token.lower

    def print_summary(self, most_common):
        print('SUMMARY')
        for m in most_common:
            print(f'{spacy_.convert_to_string(m[0])} : {m[1]}')
        print('\n\n\n')

    def display_output(self, number):
        for orth, count, matches in self.get_most_common(number):
            print(f'\n\nFound {count} instances of "{spacy_.convert_to_string(orth)}"')
            for m in matches:
                print(f'\nIn {self.loader.file_paths[m.doc_id]}')
                print(m.format_sentence(self.sents))
