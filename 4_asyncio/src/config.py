import os
from datetime import date

from dotenv import load_dotenv

load_dotenv()


# General config
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database config
DB_NAME = os.environ.get('DB_NAME')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')

# Logger config
LOG_DIR = BASE_DIR + '/logs/'
LOG_FORMAT = '%(asctime)s [%(levelname)s] %(funcName)s %(message)s'
LOGFILE_MAXSIZE = 1024 * 1024
LOGFILES_MAX = 10

# Parser config
START_DATE = date(year=2023, month=1, day=1)
END_DATE = date.today()
LOCAL_DIR = BASE_DIR + '/spimex_sync/'
LOCAL_DIR_ASYNC = BASE_DIR + '/spimex_async/'
URL = 'https://spimex.com/upload/reports/oil_xls/'
FILENAME = 'oil_xls_{year}{month}{day}162000.xls'
SHEET_NAME = 'TRADE_SUMMARY'
START_ROW = 'Единица измерения: Метрическая тонна'
STOP_ROW = 'Итого:'

# Parser messages
class ParsMsg:
    PARSER_START = 'Parser started'
    GETMISSINGFILES_START = ('Parser started generating a list '
                             'of files to be downloaded')
    GETFILES_START = ('Parser started generating a list '
                      'of files to be added to database')
    GETFILES_DONE = 'Parser completed generating a list of files'
    DOWNLOADFILES_START = 'Parser started downloading files'
    DOWNLOADFILES_200 = 'Downloaded file'
    DOWNLOADFILES_404 = 'Got 404 for file'
    DOWNLOADFILES_DONE = 'Parser completed downloading files'
    ADDTODB_START = 'Parser started adding files to database'
    ADDTODB_FILEOK = 'Processed and added file'
    ADDTODB_FILESOK = ('Parser completed adding files to database '
                       'and will now commit them')
    ADDTODB_DONE = 'Parser committed the changes to database'
    PARSER_DONE = 'Parser has completed its work'
    PARSER_REPORT = 'Total elapsed time: '
