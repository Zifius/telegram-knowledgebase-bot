from sqlalchemy import Table, Column, ForeignKey,  Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    quotes = relationship('Quote', back_populates='user')


class Channel(Base):
    __tablename__ = 'channel'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))


class Quote(Base):
    __tablename__ = 'quote'
    id = Column(Integer, primary_key=True)
    term = Column(String(250))
    definition = Column(Text)
    created = Column(DateTime)
    updated = Column(DateTime)


association_table = Table('channel_quote', Base.metadata,
    Column('channel', Integer, ForeignKey('channel.id')),
    Column('quote', Integer, ForeignKey('quote.id'))
)

# Create an engine that stores data in the local directory's
# bot.db file.
engine = create_engine('sqlite:///bot.sqlite')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
