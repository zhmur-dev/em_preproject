from sqlalchemy import Column, create_engine, DateTime, Integer, String
from sqlalchemy.orm import DeclarativeBase, Session

from . import parser
from . import utils
from .config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER, LOCAL_DIR
from .logger import logger


DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

class Base(DeclarativeBase): pass


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


def add_to_db(files):
    """
    Adds info to database from a list of local files
    """
    with Session(autoflush=False, bind=engine) as db:
        for file in files:
            df = parser.get_data(LOCAL_DIR + file)
            for _, row in df.iterrows():
                exchange_product_id = str(row.iloc[0])
                db.add(
                    SpimexTradingResults(
                        exchange_product_id=exchange_product_id,
                        exchange_product_name=row.iloc[1],
                        oil_id=exchange_product_id[:4],
                        delivery_basis_id=exchange_product_id[4:7],
                        delivery_basis_name=row.iloc[2],
                        delivery_type_id=exchange_product_id[-1],
                        volume=row.iloc[3],
                        total=row.iloc[4],
                        count=row.iloc[5],
                        date=utils.filename_to_date(file),
                        created_on=utils.get_current_time(),
                        updated_on=utils.get_current_time()
                    )
                )
            logger.info(
                f'Finished processing {file}.'
            )
        db.commit()
        logger.info('Database populated successfully.')
