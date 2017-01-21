import word_aggregator.spacy_service as spacy_


class ConsoleFormatter(object):
    """Class for formatting output for display in terminal."""

    def __init__(self):
        self.most_common_matches = None

    def display_output(self, matches, filepaths):
        """Print the results to screen."""
        self.most_common_matches = matches
        self.print_summary()
        self.print_breakdown()

    def print_breakdown(self):
        """Print a breakdown of the most commonly occurring words."""
        for orth, count, matches in self.most_common_matches:
            print(f'\n\nFound {count} instances of "{spacy_.convert_to_string(orth)}"')
            for m in matches:
                print(f'\nIn {filepaths[m.doc_id]}')
                print(m.format_sentence(self.sents))

    def print_summary(self):
        """Print a summary of the most commonly occurring words."""
        print('SUMMARY')
        for m in self.most_common_matches:
            print(f'{spacy_.convert_to_string(m[0])} : {m[1]}')
        print('\n\n\n')
