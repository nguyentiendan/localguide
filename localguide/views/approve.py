from docutils.core import publish_parts
from sqlalchemy.sql import select, and_, or_
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
import os, uuid, shutil, random, string, json
import urllib.request
from sqlalchemy.exc import DBAPIError
from pyramid.httpexceptions import HTTPFound, HTTPNotFound,  HTTPForbidden
from ..models.user import User
from ..models.approve import Approve
from ..services.user_service import UserService
from ..services.approve_service import ApproveService

#For send mail
from pyramid_mailer.message import Message
from pyramid_mailer.mailer import Mailer
from pyramid_mailer import get_mailer

@view_config(route_name='approve_action', match_param='action=becomeguide', renderer='localguide:templates/approve/user_approve.jinja2')
def user_approve(request):
    print("APPROVE BECOME GUIDE")
    uid = request.unauthenticated_userid 
    User = UserService.by_uid_all(uid, request)
    
    if User is None :
        raise exception_response(404)
    if UserService.check_login(request) == False:
        raise exception_response(404)
    return dict(user=User)
    

@view_config(route_name='approve_action', match_param='action=publishtour', renderer='localguide:templates/approve/tour_approve.jinja2')
def tour_approve(request):
    print("APPROVE PUBLISH TOUR")
    return {}    

@view_config(route_name='approve_action', match_param='action=sendRequestBecomeGuide')
def sendRequestBecomeGuide(request):
    print("SEND REQUEST BECOME GUIDE")
    
    uid = request.unauthenticated_userid
    if uid is None :
        raise exception_response(404)
    else:
        app = Approve()
        if request.method == 'POST' :
            next_url = '/approve/becomeguide'
            data = request.json_body
            app.uid     = uid
            app.type    = '0'
            app.content = data['content']
            if ApproveService.check_exist(uid, request) == False :  #request is not send 
                try :
                    request.dbsession.add(app)
                except DBAPIError:
                    return Response(db_err_msg, content_type='text/plain', status=500)            
            else :
                return Response('NG', content_type='text/plain')    
        return Response(
                '',
                headers=[
                    ('X-Relocate', next_url),
                    ('Content-Type', 'text/html'),
                ]
        )   
        
