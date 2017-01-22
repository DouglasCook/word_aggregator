"""
Process a directory containing text files and return data on the most commonly
occurring words.

Usage:
    main.py <directory> <n_words> [--lemmatise]

Options:
    directory       directory containing files to process
    n_words         number of words to display results for
    --lemmatise     aggregate words based on their lemma instead of whole token
"""
from docopt import docopt

from word_aggregator.processor import Processor
from word_aggregator.loaders import TextFileLoader
from word_aggregator.formatters import ConsoleFormatter


def main(directory, n_words, lemmatise):
    loader = TextFileLoader(directory)
    formatter = ConsoleFormatter()
    processor = Processor(loader, formatter, lemmatise=lemmatise)
    processor.process_documents()
    processor.display_results(n_words)


if __name__ == '__main__':
    args = docopt(__doc__)
    main(args['<directory'], args['<n_words>'], args['--lemmatise'])
