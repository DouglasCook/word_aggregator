from word_aggregator.processor import Processor
from word_aggregator.loaders import TextFileLoader
from word_aggregator.formatters import ConsoleFormatter


# TODO add command line arg
LOADER = TextFileLoader('/docs')
FORMATTER = ConsoleFormatter()
PROCESSOR = Processor(LOADER, FORMATTER, lemmatise=True)
PROCESSOR.process_documents()
PROCESSOR.display_results(30)
