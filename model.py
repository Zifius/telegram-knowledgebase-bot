from sqlalchemy import Table, Column, ForeignKey,  Integer, String, Text, DateTime
from sqlalchemy.orm import relationship, sessionmaker, backref, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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

    def __init__(self, term, content):
        self.term = term
        self.content = content


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
_SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(_SessionFactory)


def session_factory():
    return _SessionFactory()


class DefinitionRepo:
    """Repo for our deffs"""

    def persist(self, quote):
        """TODO: add update / create time"""
        Session().add(quote)

    def delete(self, object_id):
        Session().delete(self.findById(object_id))

    def findByTerm(self, term):
        return Session().query(Definition).filter_by(term=term).scalar()

    def findAll(self):
        return Session().query(Definition).order_by(Definition.id)

    def findById(self, objectid):
        return Session().query(Definition).filter_by(id=objectid).scalar()


class UserRepo:
    """Repo for our quotes"""

    def persist(self, user):
        Session().add(user)

    def delete(self, object_id):
        Session().delete(self.findById(object_id))

    def findById(self, objectid):
        return Session().query(User).filter_by(id=objectid).scalar()


definitionRepo = DefinitionRepo()
userRepo = UserRepo()


