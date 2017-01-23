"""Singleton logger for all modules to use."""
import logging

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
file_handler = logging.FileHandler('log.log')
file_handler.setFormatter(formatter)
stdout_handler = logging.StreamHandler()
stdout_handler.setFormatter(formatter)

logger = logging.Logger('word_aggregator', level=logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(stdout_handler)
