import os
from datetime import datetime as dt

from dotenv import load_dotenv

load_dotenv()


# General config
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCAL_DIR = BASE_DIR + '/spimex/'
FILENAME = 'oil_xls_{year}{month}{day}162000.xls'

# Database config
DB_NAME = os.environ.get('DB_NAME')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')

# Logger config
LOG_DIR = BASE_DIR + '/logs/'
LOG_FILE = 'log.txt'
LOG_FORMAT = '%(asctime)s [%(levelname)s] %(funcName)s %(message)s'
LOGFILE_MAXSIZE = 1024 * 1024
LOGFILES_MAX = 10

# Parser config
START_DATE = dt(year=2023, month=1, day=1)
END_DATE = dt(year=dt.now().year, month=dt.now().month, day=dt.now().day)
URL = 'https://spimex.com/upload/reports/oil_xls/'
SHEET_NAME = 'TRADE_SUMMARY'
START_ROW = 'Единица измерения: Метрическая тонна'
STOP_ROW = 'Итого:'
