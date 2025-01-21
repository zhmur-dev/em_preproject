import os
from datetime import date, datetime as dt

import pandas as pd
import requests
from sqlalchemy.orm import Session

from .config import (
    END_DATE, FILENAME, LOCAL_DIR, ParsMsg, SHEET_NAME,
    START_DATE, START_ROW, STOP_ROW, URL
)
from .database import engine, SpimexTradingResults
from .logger import logger


def date_to_filename(date_obj):
    """
    Returns a string containing the name of .xls file
    for a provided date object
    """
    month = str(date_obj.month) if len(str(date_obj.month)) > 1 \
        else '0' + str(date_obj.month)
    day = str(date_obj.day) if len(str(date_obj.day)) > 1 \
        else '0' + str(date_obj.day)
    return FILENAME.format(year=str(date_obj.year), month=month, day=day)


def get_files(missing=False):
    """
    Returns a list of found files when missing is set to False,
    or a list of missing files when missing is set to True
    """
    logger.info(ParsMsg.GETMISSINGFILES_START) if missing \
        else logger.info(ParsMsg.GETFILES_START)
    files = []
    date_range = pd.date_range(start=START_DATE, end=END_DATE, freq='D')
    for date_obj in date_range:
        filename = date_to_filename(date_obj)
        if (
                os.path.exists(LOCAL_DIR + filename)
                and os.path.isfile(LOCAL_DIR + filename)
        ):
            if missing is False:
                files.append(filename)
        else:
            if missing is True:
                files.append(filename)
    logger.info(ParsMsg.GETFILES_DONE)
    return files


def download_files(files):
    """
    Downloads files from the provided list of filenames
    and stores them locally
    """
    logger.info(ParsMsg.DOWNLOADFILES_START)
    os.makedirs(LOCAL_DIR, exist_ok=True)
    for file in files:
        response = requests.get(URL + file)
        if response.status_code == 200:
            with open(os.path.join(LOCAL_DIR, file), 'wb') as new_file:
                new_file.write(response.content)
                logger.info(f'{ParsMsg.DOWNLOADFILES_200} {file}')
        elif response.status_code == 404:
            logger.info(f'{ParsMsg.DOWNLOADFILES_404} {file}')
    logger.info(ParsMsg.DOWNLOADFILES_DONE)


def get_dataframe(file):
    """
    Extracts parser-relevant content from an .xls file
    and returns a DataFrame object for further processing
    """
    # Read complete XLS
    df = pd.read_excel(file, sheet_name=SHEET_NAME, header=None)

    # Find start and stop rows
    start_row = df[
        df.apply(
            lambda row: row.astype(str).str.contains(
                START_ROW, na=False
            ).any(), axis=1
        )
    ].index[0] + 2
    stop_row = df.iloc[start_row + 1:].apply(
        lambda row: row.astype(str).str.contains(
            STOP_ROW, na=False
        ).any(), axis=1
    ).idxmax() - 1

    # noinspection PyTypeChecker
    # Return filtered content
    return pd.read_excel(
        file,
        sheet_name=SHEET_NAME,
        skiprows=start_row,
        nrows=stop_row - start_row,
        usecols=list(range(1, 6)) + [14]
    ).loc[lambda x: x.iloc[:, 5] != '-']


def add_to_db(files):
    """
    Adds info to database from a list of local files
    """
    logger.info(ParsMsg.ADDTODB_START)
    with Session(autoflush=False, bind=engine) as db:
        current_date = date.today()
        for file in files:
            df = get_dataframe(LOCAL_DIR + file)
            for _, row in df.iterrows():
                sheet_date = date(
                    year=int(file[8:12]),
                    month=int(file[12:14]),
                    day=int(file[14:16])
                )
                db.add(
                    SpimexTradingResults(
                        exchange_product_id=row.iloc[0],
                        exchange_product_name=row.iloc[1],
                        oil_id=row.iloc[0][:4],
                        delivery_basis_id=row.iloc[0][4:7],
                        delivery_basis_name=row.iloc[2],
                        delivery_type_id=row.iloc[0][-1],
                        volume=row.iloc[3],
                        total=row.iloc[4],
                        count=row.iloc[5],
                        date=sheet_date,
                        created_on=current_date,
                        updated_on=current_date,
                    )
                )
            logger.info(f'{ParsMsg.ADDTODB_FILEOK} {file}')
        logger.info(ParsMsg.ADDTODB_FILESOK)
        db.commit()
        logger.info(ParsMsg.ADDTODB_DONE)


def report(started_at, done_at):
    """
    Logs total elapsed time based on provided start time and end time
    """
    elapsed_time = (done_at - started_at).seconds
    logger.info(f'{ParsMsg.PARSER_REPORT}'
                f'{elapsed_time // 60} min {elapsed_time % 60} sec')

def run():
    """
    Runs standard sync_parser workflow
    """
    started_at = dt.now()
    logger.info(ParsMsg.PARSER_START)
    files = get_files(missing=True)
    download_files(files)
    add_to_db(get_files())
    done_at = dt.now()
    logger.info(ParsMsg.PARSER_DONE)
    report(started_at, done_at)
