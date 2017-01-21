from word_aggregator.processor import Processor
from word_aggregator.loader import Loader


LOADER = Loader('./docs')
PROCESSOR = Processor(LOADER, lemmatise=True)
PROCESSOR.process_documents()
PROCESSOR.display_output(30)
