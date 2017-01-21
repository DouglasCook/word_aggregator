"""Singleton spacy instance for all other modules to use."""
import spacy

NLP = spacy.load('en')
