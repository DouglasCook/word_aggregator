from collections import Counter, namedtuple

import word_aggregator.spacy_service as spacy_
from word_aggregator.match import Match
from word_aggregator.logger import logger


Sentence = namedtuple('Sentence', ['id', 'doc_id', 'tokens'])
Result = namedtuple('Result', ['orth', 'count', 'matches'])


class Processor(object):
    """Class for processing documents and extracting most commonly occurring words."""

    def __init__(self, loader, formatter, lemmatise=False):
        """Constructor

        Args:
            loader: loader instance with read_files method
            formatter: formatter instance with display_output method
            lemmatise: bool flag for lemmatising tokens instead of lowering
        """
        self.loader = loader
        self.formatter = formatter
        self.lemmatise = lemmatise
        self.sents = []
        self.counter = Counter()

    def process_documents(self):
        """Build a list of sentences contained in docs and count token occurrences."""
        docs = self.load_parsed_docs()
        sent_id = 0
        for doc_id, doc in enumerate(docs):
            logger.info(f'Processing document {doc_id}')
            for sent in doc.sents:
                self.sents.append(Sentence(sent_id, doc_id, sent))
                sent_id += 1
            self.counter.update(
                [self.normalise_token(t) for t in doc if spacy_.is_interesting_word(t)])

    def load_parsed_docs(self):
        """Return parsed versions of all files from loader."""
        return spacy_.parse_docs(self.loader.read_files())

    def get_most_common_words(self, number):
        """Return list containing matches for given number of most commonly
        occurring words in corpus."""
        logger.info('Gathering most common words')
        most_common = [Result(orth, count, self.build_matches(orth))
                       for orth, count in self.counter.most_common(number)]
        return most_common

    def build_matches(self, orth):
        """Return a list of sentences containing given word."""
        all_matches = []
        for sent in self.sents:
            match_index = [t.i for t in sent.tokens if self.normalise_token(t) == orth]
            if match_index:
                all_matches.append(Match(match_index, sent.id, sent.doc_id))
        return all_matches

    def normalise_token(self, token):
        """Normalise given token."""
        if self.lemmatise:
            return token.lemma
        return token.lower

    def display_results(self, number):
        """Display results via formatter."""
        self.formatter.format_results(self.get_most_common_words(number),
                                      self.loader.file_paths,
                                      self.sents)
