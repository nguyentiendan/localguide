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
from .meta import Base

class Approve(Base):
    """ The SQLAlchemy declarative model class for a Tour object. """
    __tablename__ = 'approve'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    
    id              = Column(Integer, primary_key=True)
    uid             = Column(String(50), nullable=True)
    tour_id         = Column(Integer,  nullable=True)
    type            = Column(String(1), nullable=True)      #0:Approve become tour, #1:Approve publish tour
    content         = Column(Text,  nullable=True)
    status          = Column(String(1), default=0)  #0:not approve, #1: Approved
    ctime           = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    mtime           = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    