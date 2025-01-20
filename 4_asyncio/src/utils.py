from datetime import datetime as dt

from .config import FILENAME


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
