import os
from datetime import datetime as dt

import pandas as pd
import requests

from . import utils
from .config import (
    END_DATE, LOCAL_DIR, SHEET_NAME,
    START_DATE, START_ROW, STOP_ROW, URL
)
from .logger import logger


def get_files(missing=False):
    """
    Returns a list of found files when missing is set to False,
    or a list of missing files when missing is set to True
    """
    files = []
    date_range = pd.date_range(start=START_DATE, end=END_DATE, freq='D')
    for date in date_range:
        filename = utils.date_to_filename(
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
        response = requests.get(URL + file)
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
    # Read complete XLS and find start/stop rows
    df = pd.read_excel(file, sheet_name=SHEET_NAME, header=None)
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

    # Read relevant content only
    # noinspection PyTypeChecker
    df = pd.read_excel(
        file,
        sheet_name=SHEET_NAME,
        skiprows=start_row,
        nrows=stop_row - start_row,
        usecols=list(range(1, 6)) + [14],
    )

    # Return filtered content
    return df[df.iloc[:, 5] != '-']
