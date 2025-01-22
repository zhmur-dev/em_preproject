from .async_db import reset_database
from .config import ParsMsg
from .logger import logger


async def run():
    """
    Runs standard async_parser workflow
    """
    # Purge all metadata at start for testing purposes
    await reset_database()

    logger.info(ParsMsg.PARSER_START)
    logger.info(ParsMsg.PARSER_DONE)
