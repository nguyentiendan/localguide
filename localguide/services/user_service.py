import sqlalchemy as sa
from sqlalchemy import or_, desc, func, select 
from ..models.user import User

class UserService(object):
    
    @classmethod
    def all(cls, request):
        query = request.dbsession.query(User)
        return query.order_by(sa.desc(User.ctime))
    
    @classmethod
    def by_uid(cls, _uid, request):
        rs = request.dbsession.query(User).filter(User.uid == _uid).first()
        return rs
        
        '''
        query = request.dbsession.query(User)
        print(query) 
        return query.get(_uid)
        '''
    @classmethod
    def by_id_uid(cls, _id, _uid, request):
        rs = request.dbsession.query(User).filter(User.id == _id, User.uid == _uid, User.status == '1').first()
        return rs

    @classmethod
    def select_fullname_by_uid(cls, _uid, request):
        rs = request.dbsession.query(User.fullname).filter(User.uid == _uid).first()
        return rs

    @classmethod
    def by_email(cls, email, request):
        '''return request.dbsession.query(User.uid, User.email, User.password_hash).filter(User.email == email).first()'''
        return request.dbsession.query(User).filter(User.email == email, User.status == '1').first()
        #rs = request.dbsession.query(User).filter(User.email == email).first()
        #return rs
    
    @classmethod
    def check_login(cls, request):
        uid = request.unauthenticated_userid
        if uid is None:
            return False
        return True
    
    @classmethod
    def check_two_uid(cls, _uid, request):
        if _uid != int(request.unauthenticated_userid):
            return False
        return True
    
    @classmethod
    def get_RandomGuide(cls, request):
        #Get random Guide active
        rs = request.dbsession.query(User.id, User.uid, User.fullname, User.avatar, User.country, User.city, User.job, User.language).filter(User.status == '1').order_by(func.rand()).limit(3).all()
        return rs