import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from datetime import datetime as dt

import pandas as pd
import requests
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import Session

from database import Base, engine


# Main class
class SpimexTradingResults(Base):
    __tablename__ = 'spimex_trading_results'
    id = Column(Integer, primary_key=True, index=True)
    exchange_product_id = Column(String)
    exchange_product_name = Column(String)
    oil_id = Column(String)
    delivery_basis_id = Column(String)
    delivery_basis_name = Column(String)
    delivery_type_id = Column(String)
    volume = Column(Integer)
    total = Column(Integer)
    count = Column(Integer)
    date = Column(DateTime)
    created_on = Column(DateTime)
    updated_on = Column(DateTime)

# Purge all metadata at start for testing purposes
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# Parser constants and variables
START_DATE = dt(year=2023, month=1, day=1)
END_DATE = dt(year=dt.now().year, month=dt.now().month, day=dt.now().day)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REMOTE_DIR = 'https://spimex.com/upload/reports/oil_xls/'
LOCAL_DIR = BASE_DIR + '/spimex/'
LOG_DIR = BASE_DIR + '/logs/'
FILENAME = 'oil_xls_{year}{month}{day}162000.xls'
LOG_FILE = 'log.txt'
SHEET_NAME = 'TRADE_SUMMARY'
START_ROW = 'Единица измерения: Метрическая тонна'
STOP_ROW = 'Итого:'

# Set up logger
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(funcName)s %(message)s',
    handlers=[
        RotatingFileHandler(
            filename=LOG_DIR + LOG_FILE,
            maxBytes=1024 * 1024,
            backupCount=10,
        ),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger()


def get_current_time():
    return dt.now()


def date_to_filename(date):
    """
    Returns a string containing the name of .xls file
    for a provided datetime object
    """
    month = str(date.month) if len(str(date.month)) > 1 \
        else '0' + str(date.month)
    day = str(date.day) if len(str(date.day)) > 1 \
        else '0' + str(date.day)
    return FILENAME.format(year=str(date.year), month=month, day=day)


def filename_to_date(filename):
    """
    Returns a datetime object obtained from the provided filename
    """
    return dt(
        year=int(filename[8:12]),
        month=int(filename[12:14]),
        day=int(filename[14:16])
    )


def get_files(missing=False):
    """
    Returns a list of found files when missing is set to False,
    or a list of missing files when missing is set to True
    """
    files = []
    date_range = pd.date_range(start=START_DATE, end=END_DATE, freq='D')
    for date in date_range:
        filename = date_to_filename(
            dt(year=date.year, month=date.month, day=date.day)
        )
        if (
                os.path.exists(LOCAL_DIR + filename)
                and os.path.isfile(LOCAL_DIR + filename)
        ):
            if missing is False:
                files.append(filename)
        else:
            if missing is True:
                files.append(filename)
    return files


def download_files(files):
    """
    Downloads files from the provided list of filenames
    and stores them locally, logs all downloads
    """
    os.makedirs(LOCAL_DIR, exist_ok=True)
    for file in files:
        response = requests.get(REMOTE_DIR + file)
        if response.status_code == 200:
            with open(os.path.join(LOCAL_DIR, file), 'wb') as new_file:
                new_file.write(response.content)
                logger.info(
                    f'Successfully downloaded {file}.'
                )
        else:
            logger.info(
                f'Status code {response.status_code} for {file}.'
            )


def get_data(file):
    """
    Extracts parser-relevant content from an .xls file
    and returns a DataFrame object for further processing
    """
    # Read complete XLS
    df = pd.read_excel(file, sheet_name=SHEET_NAME, header=None)
    start_row = df[
        df.apply(
            lambda row: row.astype(str).str.contains(
                START_ROW, na=False
            ).any(), axis=1
        )
    ].index[0]

    # Read relevant content only
    df = pd.read_excel(
        file, sheet_name=SHEET_NAME, skiprows=start_row + 2
    )

    # Return filtered content
    return df[df.iloc[:, 14] != '-']


def add_to_db(files):
    """
    Adds info to database from a list of local files
    """
    with Session(autoflush=False, bind=engine) as db:
        for file in files:
            df = get_data(LOCAL_DIR + file)
            for _, row in df.iterrows():
                exchange_product_id = str(row.iloc[1])
                if exchange_product_id == STOP_ROW:
                    break
                else:
                    db.add(
                        SpimexTradingResults(
                            exchange_product_id=exchange_product_id,
                            exchange_product_name=row.iloc[2],
                            oil_id=exchange_product_id[:4],
                            delivery_basis_id=exchange_product_id[4:7],
                            delivery_basis_name=row.iloc[3],
                            delivery_type_id=exchange_product_id[-1],
                            volume=row.iloc[4],
                            total=row.iloc[5],
                            count=row.iloc[14],
                            date=filename_to_date(file),
                            created_on=get_current_time(),
                            updated_on=get_current_time()
                        )
                    )
            logger.info(
                f'Finished processing {file}.'
            )
        db.commit()
        logger.info('Database populated successfully.')


if __name__ == '__main__':
    while True:
        choice = input('Download new/missing files? (Y/N): ')
        if choice == 'Y' or choice == 'y':
            files = get_files(missing=True)
            download_files(files)
        elif choice != 'N' and choice != 'n':
            print('Sorry, try again.')
            continue
        add_to_db(get_files())
        exit()
