import logging
import os
import sys
from logging.handlers import RotatingFileHandler

from .config import (
    LOG_DIR, LOG_FORMAT, LOGFILE_MAXSIZE, LOGFILES_MAX
)


def get_logger(name):
    os.makedirs(LOG_DIR, exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(level=logging.INFO)
    file_handler = RotatingFileHandler(
            filename=LOG_DIR + name + '.log',
            maxBytes=LOGFILE_MAXSIZE,
            backupCount=LOGFILES_MAX,
    )
    screen_handler = logging.StreamHandler(sys.stdout)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    screen_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(file_handler)
    logger.addHandler(screen_handler)
    return logger
