from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from database import Base, engine


class Genre(Base):
    __tablename__ = 'genre'
    genre_id = Column(Integer, primary_key=True, index=True)
    name_genre = Column(String)


class Author(Base):
    __tablename__ = 'author'
    author_id = Column(Integer, primary_key=True, index=True)
    name_author = Column(String)


class City(Base):
    __tablename__ = 'city'
    city_id = Column(Integer, primary_key=True, index=True)
    name_city = Column(String)
    days_delivery = Column(Integer)


class Book(Base):
    __tablename__ = 'book'
    book_id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author_id = Column(Integer, ForeignKey('author.author_id'))
    genre_id = Column(Integer, ForeignKey('genre.genre_id'))
    price = Column(Integer)
    amount = Column(Integer)


class Client(Base):
    __tablename__ = 'client'
    client_id = Column(Integer, primary_key=True, index=True)
    name_client = Column(String)
    city_id = Column(Integer, ForeignKey('city.city_id'))
    email = Column(String)


class Buy(Base):
    __tablename__ = 'buy'
    buy_id = Column(Integer, primary_key=True, index=True)
    buy_description = Column(String)
    client_id = Column(Integer, ForeignKey('client.client_id'))


class Step(Base):
    __tablename__ = 'step'
    step_id = Column(Integer, primary_key=True, index=True)
    name_step = Column(String)


class BuyBook(Base):
    __tablename__ = 'buy_book'
    buy_book_id = Column(Integer, primary_key=True, index=True)
    buy_id = Column(Integer, ForeignKey('buy.buy_id'))
    book_id = Column(Integer, ForeignKey('book.book_id'))
    amount = Column(Integer)


class BuyStep(Base):
    __tablename__ = 'buy_step'
    buy_step_id = Column(Integer, primary_key=True, index=True)
    buy_id = Column(Integer, ForeignKey('buy.buy_id'))
    step_id = Column(Integer, ForeignKey('step.step_id'))
    date_step_beg = Column(DateTime)
    date_step_end = Column(DateTime)

# Purge all metadata at start for testing purposes
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
