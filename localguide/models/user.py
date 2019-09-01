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
import random
from .meta import Base


class User(Base):
    """ The SQLAlchemy declarative model class for a User object. """
    __tablename__ = 'user'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    
    id              = Column(Integer, primary_key=True)
    uid             = Column(String(50), nullable=False, unique=True, index=True)
    fullname        = Column(String(100), nullable=False)
    avatar          = Column(String(255), nullable=True, index=True)
    email           = Column(String(100), nullable=False, unique=True)
    mobile          = Column(String(12), nullable=True, default='08012345678')
    password_hash   = Column(String(255), nullable=False)
    job             = Column(String(50), nullable=True, default='')
    sex             = Column(String(1),  nullable=True, default=1, index=True) #1:Male, 0:Female
    age             = Column(String(2),   nullable=True, default=30)
    country         = Column(String(50), nullable=True)
    city            = Column(String(50), nullable=True)
    education       = Column(String(80), nullable=True, default='')    
    language        = Column(String(100), nullable=True, default='')
    work_history    = Column(Text, nullable=True)
    experience      = Column(Text, nullable=True, default='')
    hobby           = Column(String(100), nullable=True, default='')    
    skill           = Column(String(100), nullable=True, default='')
    specialities    = Column(String(100), nullable=True, default='')    
    level           = Column(String(1), default=0)  #0:junior:, 1:Senior, 2:Professsional
    status          = Column(String(1), default=0)  #0:Deactive: can not login, 1:Active
    role            = Column(String(1), default=0)  #0:Temp guide, #1:Guide, #2:Admin 
    req_active      = Column(String(1), default=0)  #0:Not request, and send request 1:Send request to admin
    active_code     = Column(String(15), nullable=True)
    last_login      = Column(DateTime, nullable=True)
    ctime           = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    mtime           = Column(DateTime, nullable=True)
    
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
    
    def random_active_code(self):
        range_start  = 10**(10-1) #random 10 digit number
        range_end    = (10**10)-1
        active_code  = random.randint(range_start, range_end)
        self.active_code = active_code
        return active_code
    
    