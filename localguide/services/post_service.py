import sqlalchemy as sa
from sqlalchemy import or_, desc, func, select 
import json, collections
from ..models.post import Post
from ..models.tour import Tour
from ..models.user import User

class PostService(object):
    
    @classmethod
    def front_postall(cls, request):
        rs = request.dbsession.query(Post, User.fullname, User.avatar).filter(Post.status == '1', Post.uid == User.uid).order_by(desc(Post.mtime)).all()
        return rs

    @classmethod
    def all_post(cls, request):
        rs = request.dbsession.query(Post.id, Post.uid, Post.title, Post.status, Post.req_active, Post.mtime, User.fullname).filter(Post.uid == User.uid).order_by(desc(Post.mtime)).all()
        return rs
    
    @classmethod
    def by_uid(cls, _uid, request):
        rs = request.dbsession.query(Post.id, Post.uid, Post.title, Post.status, Post.req_active, Post.mtime).filter(Post.uid == _uid, Post.status != '3').order_by(desc(Post.mtime)).all()
        return rs    
    
    @classmethod
    def by_id(cls, _id, request):
        rs = request.dbsession.query(Tour, User.fullname).filter(Tour.id == _id, Tour.uid == User.uid, Tour.status == '1').first()
        return rs

    @classmethod
    def by_id_uid(cls, _id, _uid, request):
        rs = request.dbsession.query(Post).filter(Post.id == _id, Post.uid == _uid).first()
        return rs
    
    @classmethod
    def delete_by_id_uid(cls, _id, _uid, request):
        rs = request.dbsession.query(Post).filter(Post.id == _id, Post.uid == _uid).delete()
        return rs

    @classmethod
    def update_by_id_uid(cls, _id, _uid, request):
        rs = request.dbsession.query(Post).filter(Post.id == _id, Post.uid == _uid).first()
        return rs

    @classmethod
    def detail_by_id_uid(cls, _id, _uid, request):        
        rs = request.dbsession.query(Tour, User.id, User.fullname, User.avatar, User.level).filter(Tour.id == _id, Tour.uid == _uid, Tour.uid == User.uid, Tour.status == '1').first()
        return rs

    
    
