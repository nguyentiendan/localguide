import bcrypt
import datetime
from sqlalchemy import (
    Column,
    String,
    Integer,
    Text,
    DateTime,
    Unicode,     #<- will provide Unicode field
    UnicodeText, #<- will provide Unicode text field
    func
)
from sqlalchemy.ext.indexable import index_property
from webhelpers2.text import urlify #<- will generate slugs
from webhelpers2.date import distance_of_time_in_words #<- human friendly dates
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from .meta import Base

class Orders(Base):
    """ The SQLAlchemy declarative model class for a Tour object. """
    __tablename__ = 'orders'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    
    id              = Column(Integer, primary_key=True)
    uid             = Column(String(50), nullable=False)
    tour_id         = Column(Integer, nullable=False)
    tour_title      = Column(String(50), nullable=False)
    tour_price      = Column(Integer, nullable=True)
    tour_currency   = Column(String(5), nullable=True)
    charge_id       = Column(String(50), nullable=False)
    name_card       = Column(String(50), nullable=False)
    email           = Column(String(50), nullable=False)
    phone           = Column(String(12), nullable=False)
    status          = Column(String(50), nullable=True)
    ctime           = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    mtime           = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    
