from spacy.lexeme import Lexeme

from word_aggregator.spacy_instance import NLP


def convert_to_string(orth):
    return NLP.vocab.strings[orth]


def convert_to_lexeme(orth):
    return Lexeme(NLP.vocab, orth)


def is_good_word(word):
    return word.is_alpha and not word.is_stop
