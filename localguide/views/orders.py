from docutils.core import publish_parts
from sqlalchemy.sql import select, and_, or_, func
from pyramid.response import Response
from pyramid.httpexceptions import exception_response

from pyramid.security import (
    remember,
    forget,
    )
from pyramid.view import (
    forbidden_view_config,
    view_config,
)
import os, uuid, shutil, random, string, json, datetime
import urllib.request
from sqlalchemy.exc import DBAPIError
from pyramid.httpexceptions import HTTPFound, HTTPNotFound,  HTTPForbidden
from ..models.tour import Tour
from ..models.user import User
from ..models.orders import Orders
from ..services.user_service import UserService
from ..services.tour_service import TourService
from ..services.orders_service import OrdersService
from ..utils import XssHtml
import stripe

'''
@view_config(route_name='orders_action', match_param='action=refund')
def orders_refund(request):
    print('ORDERS REFUND')
    user = request.user 
    data = request.json_body
    charge_id  = data['charge_id']    #charge_ID
    price  = data['price']  #Price
    
    #check only admin/tour admin access this function
    if user is None or charge_id is None or UserService.isAdmin(request) == False:
        raise exception_response(404)
    else :
        stripe.api_key = 'sk_test_zhVLqm2IiBSzHCmYZbJwlwB400fY8QkLs2'
        print(charge_id)
        print(price)
    
        return Response(
            charge.status,
            headers=[
                ('X-Relocate', ''),
                ('Content-Type', 'text/html'),
            ]
        )
'''    
    
