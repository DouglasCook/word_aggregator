"""
Process a directory containing text files and return data on the most commonly
occurring words.

Usage:
    main.py <directory> <n_words> [--csv_output] [--lemmatise]

Options:
    directory       directory containing files to process
    n_words         number of words to display results for
    --csv_output    write results to csv instead of screen
    --lemmatise     aggregate words based on their lemma instead of whole token
"""
from docopt import docopt

from word_aggregator.processor import Processor
from word_aggregator.loaders import TextFileLoader
from word_aggregator.formatters import ConsoleFormatter, CsvFormatter


def main(directory, n_words, csv_output, lemmatise):
    loader = TextFileLoader(directory)
    formatter = CsvFormatter if csv_output else ConsoleFormatter
    processor = Processor(loader, formatter(), lemmatise=lemmatise)
    processor.process_documents()
    processor.display_results(n_words)


if __name__ == '__main__':
    args = docopt(__doc__)
    main(args['<directory>'], int(args['<n_words>']), args['--csv_output'],
         args['--lemmatise'])
