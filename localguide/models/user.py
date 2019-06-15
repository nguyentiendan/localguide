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
import hashlib 
from .meta import Base


class User(Base):
    """ The SQLAlchemy declarative model class for a User object. """
    __tablename__ = 'user'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    
    id              = Column(Integer, primary_key=True)
    uid             = Column(String(50), nullable=False, unique=True)
    fullname        = Column(String(100), nullable=False)
    avatar          = Column(String(255), nullable=True)
    email           = Column(String(100), nullable=False, unique=True)
    mobile          = Column(String(12), nullable=True, default='08012345678')
    password_hash   = Column(String(255), nullable=False)
    job             = Column(String(50), nullable=True)
    sex             = Column(String(1),  nullable=True, default=1, index=True) #1:Male, 0:Female
    age             = Column(String(2),   nullable=True, default=30)
    country         = Column(String(50), nullable=True, index=True)
    city            = Column(String(50), nullable=True, index=True)
    education       = Column(String(80), nullable=True)    
    language        = Column(String(100), nullable=True)
    work_history    = Column(Text, nullable=True)
    experience      = Column(Text, nullable=True)
    hobby           = Column(String(100), nullable=True)    
    skill           = Column(String(100), nullable=True)
    specialities    = Column(String(100), nullable=True)    
    level           = Column(String(1), default=0)  #0:junior:, 1:Senior, 2:Professsional
    status          = Column(String(1), default=1)  #0:Deactive: can not login, 1:Active
    role            = Column(String(1), default=0)  #0:User, #1:Guide, #2:Admin 
    #approve         = Column(String(1), default=0)  #0:Not appove, #1:Approve request, #2 Approved
    last_login      = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    ctime           = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    mtime           = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    
    @property
    def slug(self):
        return urlify(self.title)

    @property
    def created_in_words(self):
        return distance_of_time_in_words(self.created, datetime.datetime.utcnow())
    
    def set_password(self, pw):
        pwhash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
        self.password_hash = pwhash.decode('utf8')

    def check_password(self, pw):
        if self.password_hash is not None:
            expected_hash = self.password_hash.encode('utf8')
            return bcrypt.checkpw(pw.encode('utf8'), expected_hash)
        return False
    '''
    def verify_password(self, password):
        # is it cleartext?
        if password == self.password:
            self.set_password(password)

        return blogger_pwd_context.verify(password, self.password)
    '''
    def random_uid(self):
        uid = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
        uid = hashlib.sha1(uid.encode()).hexdigest()  
        self.uid = uid
        return uid

    