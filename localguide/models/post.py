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

class Post(Base):
    """ The SQLAlchemy declarative model class for a Tour object. """
    __tablename__ = 'post'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    
    id              = Column(Integer, primary_key=True)
    uid             = Column(String(50), nullable=False)
    title           = Column(String(50), nullable=False)
    content         = Column(Text, nullable=False)
    status          = Column(String(1), default=0)  #0:Deactive : not active, 1:Active : show on homepage, 2:Disable : not show on homepage and guide can active again, 3:Delete
    req_active      = Column(String(1), default=0)  #0:Not request,  1:Send request to admin
    ctime           = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    mtime           = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    
    
    @property
    def created_in_words(self):
        return distance_of_time_in_words(self.mtime, datetime.datetime.utcnow(),granularity='day')
    