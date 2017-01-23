"""Singleton spacy instance for all other modules to use."""
import spacy
from spacy.lexeme import Lexeme

from word_aggregator.logger import logger

logger.info('Loading spacy assets')
NLP = spacy.load('en')


def parse_docs(files):
    """Return all parsed files as generator."""
    return NLP.pipe(files)


def convert_to_string(orth):
    """Return a string given its orth id."""
    return NLP.vocab.strings[orth]


def is_interesting_word(word):
    """Return false for punctuation or stopword tokens."""
    return word.is_alpha and not word.is_stop
