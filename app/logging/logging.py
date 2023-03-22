import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
DT_FORMAT = '%d.%m.%Y %H:%M:%S'
BASE_DIR = Path(__file__).parent


def configure_logging():
    log_dir = BASE_DIR
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / 'cat_charity_fund.log'

    rotating_handler = RotatingFileHandler(log_file, maxBytes=10 ** 6, backupCount=5, encoding='utf-8')

    logging.basicConfig(
        datefmt=DT_FORMAT,
        format=LOG_FORMAT,
        level=logging.INFO,
        handlers=(rotating_handler, logging.StreamHandler())
    )