import sqlalchemy as sa
from sqlalchemy import or_, desc, func, select 
from ..models.approve import Approve

class ApproveService(object):
    
    @classmethod
    def all(cls, request):
        query = request.dbsession.query(Approve)
        return query.order_by(sa.desc(Approve.ctime))
    
    @classmethod
    def check_exist(cls, _uid, request):
        rs = request.dbsession.query(Approve.uid).filter(Approve.uid == _uid).first()
        if rs is not None: # send request already
            return True
        return False

    @classmethod
    def by_id_uid(cls, _id, _uid, request):
        rs = request.dbsession.query(Approve).filter(Approve.id == _id, Approve.uid == _uid, Approve.status == '1').first()
        return rs