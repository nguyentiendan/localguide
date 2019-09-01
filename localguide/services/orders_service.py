import sqlalchemy as sa
from sqlalchemy import or_, desc, func, select 
import json, collections
from ..models.tour import Tour
from ..models.user import User
from ..models.orders import Orders

class OrdersService(object):
     
    @classmethod
    def all_orders(cls, request):
        rs = request.dbsession.query(Orders).order_by(desc(Orders.mtime)).all()
        return rs

    @classmethod
    def by_uid(cls, _uid, request):
        rs = request.dbsession.query(Orders).filter(Orders.uid == _uid).all()
        return rs

    @classmethod
    def update_by_id_uid_chargeid(cls, tour_id, _uid, charge_id, request):
        rs = request.dbsession.query(Orders).filter(Orders.tour_id == tour_id, Orders.uid == _uid, Orders.charge_id == charge_id).first()
        return rs
    