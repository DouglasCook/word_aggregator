from word_aggregator.processor import Processor
from word_aggregator.loader import TextFileLoader
from word_aggregator.formatter import ConsoleFormatter


LOADER = TextFileLoader('./docs')
FORMATTER = ConsoleFormatter()
PROCESSOR = Processor(LOADER, FORMATTER, lemmatise=True)
PROCESSOR.process_documents()
PROCESSOR.display_results(30)
