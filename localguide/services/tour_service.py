import sqlalchemy as sa
from sqlalchemy import or_, desc, func, select 
import json, collections
from ..models.tour import Tour
from ..models.user import User

class TourService(object):
    
    @classmethod
    def admin_tourall(cls, request):
        query = request.dbsession.query(Tour)
        return query.order_by(sa.desc(Tour.mtime))
        #rs = request.dbsession.query(Tour).order_by(sa.desc(Tour.mtime)).all()
        #return rs
        
    @classmethod
    def front_tourall(cls, request):
        rs = request.dbsession.query(Tour).filter(Tour.status == '1').order_by(desc(Tour.mtime)).all()
        return rs
    
    @classmethod
    def by_id(cls, _id, request):
        rs = request.dbsession.query(Tour, User.fullname).filter(Tour.id == _id, Tour.uid == User.uid, Tour.status == '1').first()
        return rs

    @classmethod
    def by_id_uid(cls, _id, _uid, request):
        rs = request.dbsession.query(Tour).filter(Tour.id == _id, Tour.uid == _uid).first()
        return rs

    @classmethod
    def detail_by_id_uid(cls, _id, _uid, request):
        # Lay them User.fullname , tham khảo by_id
        rs = request.dbsession.query(Tour, User.fullname, User.avatar).filter(Tour.id == _id, Tour.uid == _uid, Tour.uid == User.uid).first()
        return rs

    @classmethod
    def by_uid(cls, _uid, request):
        # Lay them User.fullname , tham khảo by_id
        rs = request.dbsession.query(Tour).filter(Tour.uid == _uid).all()
        return rs    
    
    @classmethod
    def delete_id_uid(cls, _id, _uid, request):
        rs = request.dbsession.query(Tour).filter(Tour.id == _id, Tour.uid == _uid).delete()
        return rs
    
    @classmethod
    def get_TourNotActive(cls, _uid, request):
        rs = request.dbsession.query(Tour).filter(Tour.uid == _uid, Tour.status == '0').order_by(desc(Tour.mtime)).all()
        return rs
    
    @classmethod
    def get_RandomTour(cls, request):
        #Get random Tour adtive
        rs = request.dbsession.query(Tour.id, Tour.uid, Tour.title, Tour.type, Tour.short_desc, Tour.price, Tour.days, Tour.banner).filter(Tour.status == '1').order_by(func.rand()).limit(3).all()
        return rs

    @classmethod
    def get_TourActive(cls, _uid, request):
        rs = request.dbsession.query(Tour).filter(Tour.uid == _uid, or_(Tour.status == '1', Tour.status == '2') ).order_by(desc(Tour.mtime)).all()
        return rs
    
