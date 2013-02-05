from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    ForeignKey
    )

from sqlalchemy.orm import relationship

import datetime

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_id = Column(Text, unique=True)
    name = Column(Text, unique=True)

    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

class Occurance(Base):
    __tablename__ = 'occurances'
    id = Column(Integer, primary_key=True)
    time = Column(DateTime, default=datetime.datetime.utcnow)
    event_type_id = Column(Integer, ForeignKey('event_types.id'))
    event_type = relationship("EventType")

    def __init__(self, username):
        self.username = username

class EventType(Base):
    __tablename__ = 'event_types'
    id = Column(Integer, primary_key=True)
    creator_id = Column(Integer, ForeignKey('users.id'))
    creator = relationship("User")
    name = Column(Text, unique=True)

    def __init__(self,  creator_id, name):
        self.creator_id = creator_id
        self.name = name
