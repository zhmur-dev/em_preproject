import logging
import os
import sys
from logging.handlers import RotatingFileHandler

from .config import (
    LOG_DIR, LOG_FILE, LOG_FORMAT, LOGFILE_MAXSIZE, LOGFILES_MAX
)


os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        RotatingFileHandler(
            filename=LOG_DIR + LOG_FILE,
            maxBytes=LOGFILE_MAXSIZE,
            backupCount=LOGFILES_MAX,
        ),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger()
