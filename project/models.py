import datetime
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class EventType(Base):
    __tablename__ = 'event_types'

    eid = Column(Integer, primary_key=True)
    name = Column(Unicode(255), unique=True)

    def __init__(self, name):
        self.name = name


class Occurance(Base):
    __tablename__ = 'occurances'

    oid = Column(Integer, primary_key=True)
    creator_id = Column(Integer, ForeignKey('users.uid'))
    event_type_id = Column(Integer, ForeignKey('event_types.eid'))
    time = Column(DateTime, default=datetime.datetime.utcnow)

    creator = relationship("User", backref="occurances")
    event_type = relationship(
        "EventType",
        backref="occurances",
        lazy='joined',
        uselist=False
    )

    def __init__(self, creator, event_type):
        self.creator = creator
        self.event_type = self.event_type


class User(Base):
    __tablename__ = 'users'

    uid = Column(Integer, primary_key=True)
    user_id = Column(Unicode(255), unique=True)
    name = Column(Unicode(500), unique=True)

    def __init__(self, user_id, name):
        self.user_id = user_id
