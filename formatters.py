from collections import Counter

import word_aggregator.spacy_service as spacy_


class ConsoleFormatter(object):
    """Class for formatting output for display in terminal."""

    def __init__(self):
        self.most_common_matches = None

    def display_output(self, matches, filepaths, sentences):
        """Print the results to screen."""
        self.most_common_matches = matches
        self.print_summary()
        self.print_breakdown(filepaths, sentences)

    def print_breakdown(self, filepaths, sentences):
        """Print a breakdown of the most commonly occurring words."""
        doc_id = None
        for orth, count, matches in self.most_common_matches:
            print(f'\n\n----------- '
                  f'Found {count} instances of "{spacy_.convert_to_string(orth)}"')
            doc_counts = Counter([m.doc_id for m in matches])
            for m in matches:
                # we know the matches are ordered by document
                if m.doc_id != doc_id:
                    print(f'\n----------- Found {doc_counts[m.doc_id]} times in '
                          f'{filepaths[m.doc_id]}\n')
                    doc_id = m.doc_id
                print(m.format_sentence(sentences))

    def print_summary(self):
        """Print a summary of the most commonly occurring words."""
        print('SUMMARY OF WORD COUNTS')
        for m in self.most_common_matches:
            print(f'{spacy_.convert_to_string(m[0])} : {m[1]}')
        print('\n')
