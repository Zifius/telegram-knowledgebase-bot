from datetime import datetime
from sqlalchemy import Column, ForeignKey,  Integer, String, Text, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from base import Base, Session


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, index=True, unique=True)
    name = Column(String(250))

    def __init__(self, telegram_id, name):
        self.telegram_id = telegram_id
        self.name = name

    @staticmethod
    def find(telegram_id):
        results = Session().query(User).filter_by(telegram_id=telegram_id).first()
        return results

    @staticmethod
    def insert(telegram_id, name):
        user = User(telegram_id, name)
        Session().add(user)
        return user

    @staticmethod
    def find_create(telegram_id, name):
        user = User.find(telegram_id)
        if not user:
            user = User.insert(telegram_id, name)
        return user


class Channel(Base):
    __tablename__ = 'channel'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    telegram_id = Column(Integer, index=True, unique=True)

    def __init__(self, telegram_id, name):
        self.telegram_id = telegram_id
        self.name = name

    @staticmethod
    def insert(telegram_id, name):
        channel = Channel(telegram_id, name)
        Session().add(channel)
        return channel

    @staticmethod
    def find_create(telegram_id, name):
        channel = Channel.find(telegram_id)
        if not channel:
            channel = Channel.insert(telegram_id, name)
        return channel

    @staticmethod
    def find(telegram_id):
        return Session().query(Channel).filter_by(telegram_id=telegram_id).first()


class Definition(Base):
    __tablename__ = 'definition'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    # create 1 to many relationship
    user = relationship('User', backref='user')
    channel_id = Column(Integer, ForeignKey('channel.id'), index=True)
    channel = relationship('Channel', backref='channel')
    term = Column(String(250), nullable=False)
    content = Column(Text, nullable=False)
    created = Column(DateTime, nullable=False)
    updated = Column(DateTime, onupdate=datetime.now)

    __table_args__ = (UniqueConstraint('channel_id', 'term', name='channel_term_uc'),)

    def __init__(self, term, content, user, channel):
        self.user = user
        self.channel = channel
        self.term = term
        self.content = content
        self.created = datetime.now()

    @staticmethod
    def find_term(channel_telegram_id, term):
            return Session().query(Definition).join(Channel)\
                .filter(Channel.telegram_id == channel_telegram_id)\
                .filter(Definition.term == term)\
                .first()

    @staticmethod
    def find_all(channel_telegram_id):
        return Session().query(Definition).join(Channel) \
                .filter(Channel.telegram_id == channel_telegram_id) \
                .order_by(Definition.id) \
                .all()

    @staticmethod
    def insert(user, channel, term, term_content):
        definition = Definition(term, term_content, user, channel)
        Session().add(definition)
        return definition

    @staticmethod
    def insert_update(user, channel, term, term_content):
        definition = Definition.find_term(channel.telegram_id, term)
        if not definition:
            Definition.insert(user, channel, term, term_content)
        else:
            definition.content = term_content
            definition.user = user


