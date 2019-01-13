from sqlalchemy import Table, Column, ForeignKey,  Integer, String, Text, DateTime
from sqlalchemy.orm import relationship, sessionmaker, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    definitions = relationship('Definition', cascade="all,delete-orphan",
                               backref=backref('user', cascade='all,delete-orphan', single_parent=True))


class Channel(Base):
    __tablename__ = 'channel'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))


class Definition(Base):
    __tablename__ = 'definition'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    term = Column(String(250))
    content = Column(Text)
    created = Column(DateTime)
    updated = Column(DateTime)


association_table = Table('channel_definition', Base.metadata,
    Column('channel', Integer, ForeignKey('channel.id')),
    Column('definition', Integer, ForeignKey('definition.id'))
)

# Create an engine that stores data in the local directory's
# bot.db file.
engine = create_engine('sqlite:///bot.sqlite')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
