import os
from datetime import date, datetime as dt

import aiohttp
import asyncio
import pandas as pd

from .async_db import AsyncSessionLocal, reset_database, SpimexTradingResults
from .config import (
    END_DATE, FILENAME, LOCAL_DIR_ASYNC, ParsMsg, SHEET_NAME,
    START_DATE, START_ROW, STOP_ROW, URL
)
from .logger import get_logger

logger = get_logger('async_parser')


def check_file_availability(file):
    """
    Checks if local file is available and returns True/False
    """
    if (
            os.path.exists(LOCAL_DIR_ASYNC + file)
            and os.path.isfile(LOCAL_DIR_ASYNC + file)
    ):
        return True
    return False


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


def get_files(start_date=START_DATE, end_date=END_DATE):
    """
    Checks files within the specified date range and returns two lists:
    - locally available files (can be parsed immediately)
    - locally unavailable files (to be downloaded / checked remotely)
    """
    logger.info(ParsMsg.GETFILES_START)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    files_to_parse = []
    files_to_download = []
    for date_obj in date_range:
        file = date_to_filename(date_obj)
        if check_file_availability(file):
            files_to_parse.append(file)
        else:
            files_to_download.append(file)
    logger.info(ParsMsg.GETFILES_DONE)
    return files_to_parse, files_to_download


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


async def download_file(session, file, queue):
    """
    Asynchronously downloads one file and adds it to the queue
    for further processing if successfully downloaded.
    """
    async with session.get(URL + file) as response:
        if response.status == 200:
            with open(os.path.join(LOCAL_DIR_ASYNC, file), 'wb') as new_file:
                new_file.write(await response.read())
            logger.info(f'{ParsMsg.DOWNLOADFILES_200} {file}')
            await queue.put(file)
        elif response.status == 404:
            logger.info(f'{ParsMsg.DOWNLOADFILES_404} {file}')


async def download_files(files, queue):
    """
    Creates tasks for files to be downloaded
    """
    logger.info(ParsMsg.DOWNLOADFILES_START)
    os.makedirs(LOCAL_DIR_ASYNC, exist_ok=True)
    async with aiohttp.ClientSession() as session:
        tasks = [download_file(session, file, queue) for file in files]
        await asyncio.gather(*tasks)
    logger.info(ParsMsg.DOWNLOADFILES_DONE)
    await queue.put(None)


async def add_to_db(queue):
    """
    Asynchronously adds parsed info to database from a queue of local files
    """
    logger.info(ParsMsg.ADDTODB_START)
    async with AsyncSessionLocal() as db:
        while True:
            try:
                file = await queue.get()
                if file is None:
                    break

                df = get_dataframe(LOCAL_DIR_ASYNC + file)
                current_date = date.today()
                sheet_date = date(
                    year=int(file[8:12]),
                    month=int(file[12:14]),
                    day=int(file[14:16])
                )

                for _, row in df.iterrows():
                    db.add(
                        SpimexTradingResults(
                            exchange_product_id=row.iloc[0],
                            exchange_product_name=row.iloc[1],
                            oil_id=row.iloc[0][:4],
                            delivery_basis_id=row.iloc[0][4:7],
                            delivery_basis_name=row.iloc[2],
                            delivery_type_id=row.iloc[0][-1],
                            volume=int(row.iloc[3]),
                            total=int(row.iloc[4]),
                            count=int(row.iloc[5]),
                            date=sheet_date,
                            created_on=current_date,
                            updated_on=current_date,
                        )
                    )
                logger.info(f'{ParsMsg.ADDTODB_FILEOK} {file}')

            except Exception as error:
                logger.error(error)
            finally:
                queue.task_done()

        logger.info(ParsMsg.ADDTODB_FILESOK)
        await db.commit()
        logger.info(ParsMsg.ADDTODB_DONE)


def report(started_at, done_at):
    """
    Logs total elapsed time based on provided start time and end time
    """
    elapsed_time = (done_at - started_at).seconds
    logger.info(f'{ParsMsg.PARSER_REPORT}'
                f'{elapsed_time // 60} min {elapsed_time % 60} sec')
    return elapsed_time


async def run():
    """
    Runs standard async_parser workflow
    """
    # Purge all metadata at start for testing purposes
    await reset_database()

    started_at = dt.now()
    logger.info(ParsMsg.PARSER_START)
    files_to_parse, files_to_download = get_files()

    queue = asyncio.Queue()
    downloader_task = asyncio.create_task(download_files(files_to_download, queue))
    db_task = asyncio.create_task(add_to_db(queue))
    for file in files_to_parse:
        await queue.put(file)

    await downloader_task
    await queue.join()
    await queue.put(None)
    await db_task

    logger.info(ParsMsg.PARSER_DONE)
    done_at = dt.now()
    return report(started_at, done_at)
