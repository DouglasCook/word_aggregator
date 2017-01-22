import csv
from datetime import datetime
from collections import Counter

import word_aggregator.spacy_service as spacy_
from word_aggregator.logger import logger


class Formatter(object):
    """Base class for formatting results of processing."""

    def format_results(self, results, filepaths, sentences):
        """Print summary of matches and perform further processing of output."""
        logger.info('Formatting results')
        self.print_summary(results)
        self.process_output(results, filepaths, sentences)

    def print_summary(self, results):
        """Print a summary of the most commonly occurring words."""
        print('SUMMARY OF WORD COUNTS')
        for m in results:
            print(f'{spacy_.convert_to_string(m[0])} : {m[1]}')
        print('\n')

    def process_output(self, results, filepaths, sentences):
        pass


class ConsoleFormatter(Formatter):
    """Class for formatting output for display in terminal."""

    def process_output(self, results, filepaths, sentences):
        """Print a breakdown of the most commonly occurring words."""
        doc_id = None
        for orth, count, matches in results:
            print(f'\n\n----------- '
                  f'Found {count} instances of "{spacy_.convert_to_string(orth)}"')

            doc_counts = Counter([m.doc_id for m in matches])
            for m in matches:
                # we know the matches are ordered by document
                if m.doc_id != doc_id:
                    doc_id = m.doc_id
                    count = doc_counts[m.doc_id]
                    doc_path = filepaths[m.doc_id]
                    print(f'\n----------- Found {count} times in {doc_path}\n')
                print(m.format_sentence(sentences))


class CsvFormatter(Formatter):
    """Class for dumping results to a CSV file."""

    def process_output(self, results, filepaths, sentences):
        """Write a csv with one row for each sentence containing a match."""
        logger.info('Writing results to CSV')

        field_names = ['word', 'document', 'sentence_number', 'hits', 'sentence']
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f'results_{now}.csv'

        with open(file_name, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=field_names)
            writer.writeheader()

            for orth, count, matches in results:
                for m in matches:
                    writer.writerow({
                        'word': orth,
                        'document': filepaths[m.doc_id],
                        'sentence_number': m.sent_id,
                        'hits': len(m.token_ids),
                        'sentence': m.format_sentence(sentences)
                    })
