"""Singleton spacy instance for all other modules to use."""
import spacy
from spacy.lexeme import Lexeme

NLP = spacy.load('en')


def parse_docs(files):
    """Return generator of all parsed files."""
    return NLP.pipe(files)


def convert_to_string(orth):
    return NLP.vocab.strings[orth]


def convert_to_lexeme(orth):
    return Lexeme(NLP.vocab, orth)


def is_good_word(word):
    return word.is_alpha and not word.is_stop
