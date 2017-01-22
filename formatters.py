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
        for res in results:
            word = spacy_.convert_to_string(res.orth)
            print(f'{word} : {res.count}')
        print('\n')


class ConsoleFormatter(Formatter):
    """Class for formatting output for display in terminal."""

    highlight_start = '\033[91m' # red
    highlight_end = '\033[0m'

    def process_output(self, results, filepaths, sentences):
        """Print a breakdown of the most commonly occurring words."""
        doc_id = None
        for res in results:
            word = spacy_.convert_to_string(res.orth)
            print(f'\n\n----------- Found {res.count} instances of "{word}"')

            doc_counts = Counter([m.doc_id for m in res.matches])
            for m in res.matches:
                # we know the matches are ordered by document
                if m.doc_id != doc_id:
                    doc_id = m.doc_id
                    doc_count = doc_counts[m.doc_id]
                    doc_path = filepaths[m.doc_id]
                    print(f'\n----------- Found {doc_count} times in {doc_path}\n')
                print(f'{m.format_sentence(sentences, self.highlight_start, self.highlight_end)}\n')


class CsvFormatter(Formatter):
    """Class for dumping results to a CSV file."""

    highlight_start = '|'
    highlight_end = '|'

    def process_output(self, results, filepaths, sentences):
        """Write a csv with one row for each sentence containing a match."""
        field_names = ['word', 'document', 'sentence_number', 'hits', 'sentence']
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f'results_{now}.csv'
        logger.info(f'Writing results to {file_name}')

        with open(file_name, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=field_names)
            writer.writeheader()

            for res in results:
                for m in res.matches:
                    writer.writerow({
                        'word': spacy_.convert_to_string(res.orth),
                        'document': filepaths[m.doc_id],
                        'sentence_number': m.sent_id,
                        'hits': len(m.token_ids),
                        'sentence': m.format_sentence(
                            sentences, self.highlight_start, self.highlight_end
                        )
                    })
