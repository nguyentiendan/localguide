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

class Tour(Base):
    """ The SQLAlchemy declarative model class for a Tour object. """
    __tablename__ = 'tour'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    
    id              = Column(Integer, primary_key=True)
    uid             = Column(String(50), nullable=False)
    title           = Column(String(50), nullable=True)
    type            = Column(String(50), nullable=True)
    short_desc      = Column(String(255), nullable=True)
    country         = Column(String(30), nullable=True)
    city            = Column(String(30), nullable=True)
    price           = Column(Integer, nullable=True)
    days            = Column(String(2), nullable=True)
    content         = Column(Text, nullable=True)
    banner          = Column(String(50), nullable=True)
    status          = Column(String(1), default=0)  #0:Deactive : not show on homepage and admin must review, 1:Active : show on homepage, 2:Disable : not show on homepage and guide can active again
    ctime           = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    mtime           = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    
    
    @property
    def created_in_words(self):
        return distance_of_time_in_words(self.mtime, datetime.datetime.utcnow(),granularity='day')
    