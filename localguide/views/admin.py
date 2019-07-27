from docutils.core import publish_parts
from sqlalchemy.sql import select, and_, or_, func
import datetime
from pyramid.response import Response
from pyramid.httpexceptions import exception_response
from pyramid.view import (forbidden_view_config, view_config,)
from sqlalchemy.exc import DBAPIError
from pyramid.httpexceptions import HTTPFound, HTTPNotFound,  HTTPForbidden
from ..models.user import User
from ..models.tour import Tour
from ..services.user_service import UserService
from ..services.tour_service import TourService
from ..utils import XssHtml

@view_config(route_name='admin_action', match_param='action=dashboard', renderer='localguide:templates/admin/dashboard.jinja2')
def admin_dashboard(request):
    print('ADMIN DASHBOARD')
    user = request.user
    #check only admin/tour admin access this function
    if user is None or UserService.isAdmin(request) == False:
        raise exception_response(404)
    
    return {} 

@view_config(route_name='admin_action', match_param='action=profile', renderer='localguide:templates/admin/profile.jinja2')
def admin_profile(request):
    print('ADMIN USER PROFILE')
    user = request.user
    #check only admin/tour admin access this function
    if user is None or UserService.isAdmin(request) == False:
        raise exception_response(404)
    else :
        User = UserService.by_uid_all(request.user.uid, request)
        if User is None :
            raise exception_response(404)   
    return {'user':User} 

@view_config(route_name='admin_action', match_param='action=changepass', renderer='localguide:templates/admin/change_password.jinja2')
def admin_changepass(request):
    print('ADMIN CHANGE PASSWORD')
    user = request.user
    #check only admin/tour admin access this function
    if user is None or UserService.isAdmin(request) == False:
        raise exception_response(404)
    
    return {} 


@view_config(route_name='admin_action', match_param='action=tourlist', renderer='localguide:templates/admin/tour_list.jinja2')
def admin_tour_list(request):
    print('TOUR LIST of GUIDE')
    user = request.user
    #check only admin/tour admin access this function
    if user is None or UserService.isAdmin(request) == False:
        raise exception_response(404)
    else :
        uid  = request.user.uid
        if request.user.role == '2':     #Admin
            tour = TourService.all_tour(request=request)
        elif request.user.role == '1':   #Tour admin
            tour = TourService.by_uid(uid, request=request)
    return {'tour':tour}

@view_config(route_name='admin_action', match_param='action= userlist', renderer='localguide:templates/admin/user_list.jinja2')
def admin_user_list(request):
    print('ADMIN USER LIST')
    user = request.user
    #check only admin access this function
    if user is None or UserService.isAdmin_2(request) == False:
        raise exception_response(404)
    else :
        user = UserService.all(request=request)
    return {'user':user}

@view_config(route_name='admin_action', match_param='action=detail', renderer='localguide:templates/admin/user_detail.jinja2')
def admin_user_detail(request):
    print('ADMIN USER DETAIL')
    user = request.user
    id  = request.params.get('id')
    uid = request.params.get('uid')
    
    #check only admin access this function
    if id is None or uid is None or user is None or UserService.isAdmin_2(request) == False:
        raise exception_response(404)
    else :
        User = UserService.user_by_id_uid(id, uid, request)
        if User is None :
            raise exception_response(404)   
    return {'user':User} 

@view_config(route_name='admin_action', match_param='action=create', renderer='localguide:templates/admin/tour_create.jinja2')
def admin_tour_create(request):
    print('TOUR CREATE')
    user = request.user
    #check only admin/tour admin access this function
    if user is None or UserService.isAdmin(request) == False:
        raise exception_response(404)

    return {}

@view_config(route_name='admin_action', match_param='action=uploadPhoto', renderer='localguide:templates/admin/tour_uploadPhoto.jinja2')
def uploadPhoto(request):
    print('UPLOAD PHOTO FOR TOUR')
    user = request.user
    id  = request.params.get('id')
    uid = request.params.get('hash')

    #check only admin/tour admin access this function
    if user is None or UserService.isAdmin(request) == False or uid != request.user.uid :
        raise exception_response(404)
        
    return {}

@view_config(route_name='admin_action', match_param='action=edit', renderer='localguide:templates/admin/tour_edit.jinja2')
def admin_tour_edit(request):
    print('TOUR EDIT')    
    id  = request.params.get('id')
    uid = request.params.get('uid')
    user = request.user
    
    #check only admin/tour admin access this function
    if user is None or UserService.isAdmin(request) == False:
        raise exception_response(404)
    else :
        if request.user.role == '2':    #Admin
            tour = TourService.by_id_uid(id, uid, request=request)
        elif request.user.role == '1':  #Tour admin
            tour = TourService.by_id_uid(id, request.user.uid, request=request)

        if tour is None :
            raise exception_response(404)
    
        return {'tour':tour}
#Admin deactive user
@view_config(route_name='admin_action', match_param='action=user_deactive')
def admin_user_deactive(request):
    print("DEACTIVE USER")
    user = request.user
    
    #check only admin access this function
    if user is None or UserService.isAdmin_2(request) == False:
        raise exception_response(404)
    else :
        data = request.json_body    
        user = User()
        user.id   = data['id']
        user.uid  = data['uid']
        user = UserService.update_by_id_uid(user.id, user.uid, request=request)
        user.status = '0'
        user.mtime  = datetime.datetime.now()
    return Response(
        '',
        headers=[
            ('X-Relocate', ''),
            ('Content-Type', 'text/html'),
        ]
    )
#Admin active user
@view_config(route_name='admin_action', match_param='action=user_active')
def admin_user_active(request):
    print("ACTIVE USER")
    user = request.user
    
    #check only admin access this function
    if user is None or UserService.isAdmin_2(request) == False:
        raise exception_response(404)
    else :
        data = request.json_body    
        user = User()
        user.id   = data['id']
        user.uid  = data['uid']
        user = UserService.update_by_id_uid(user.id, user.uid, request=request)
        user.status = '1'
        user.mtime  = datetime.datetime.now()
    return Response(
        '',
        headers=[
            ('X-Relocate', ''),
            ('Content-Type', 'text/html'),
        ]
    )
#Admin set role for user
@view_config(route_name='admin_action', match_param='action=user_setrole')
def admin_user_setrole(request):
    print("SET ROLE FOR USER")
    user = request.user
    
    #check only admin access this function
    if user is None or UserService.isAdmin_2(request) == False:
        raise exception_response(404)
    else :
        data = request.json_body    
        user = User()
        user.id     = data['id']
        user.uid    = data['uid']
        user = UserService.update_by_id_uid(user.id, user.uid, request=request)
        user.role   = data['role']
        user.mtime  = datetime.datetime.now()
    return Response(
        '',
        headers=[
            ('X-Relocate', ''),
            ('Content-Type', 'text/html'),
        ]
    )

#Admin set level for user. Normal user have not level
@view_config(route_name='admin_action', match_param='action=user_setlevel')
def admin_user_setlevel(request):
    print("SET LEVEL FOR USER")
    user = request.user
    
    #check only admin access this function
    if user is None or UserService.isAdmin_2(request) == False:
        raise exception_response(404)
    else :
        data = request.json_body    
        user = User()
        user.id     = data['id']
        user.uid    = data['uid']
        user = UserService.update_by_id_uid(user.id, user.uid, request=request)
        user.level  = data['level']
        user.mtime  = datetime.datetime.now()
    return Response(
        '',
        headers=[
            ('X-Relocate', ''),
            ('Content-Type', 'text/html'),
        ]
    )

#Admin/Tour admin disable their tour. 
@view_config(route_name='admin_action', match_param='action=tour_disable')
def admin_tour_disable(request):
    print("ADMIN DISABLE TOUR")
    user = request.user
    
    #check only admin/tour admin access this function
    if user is None or UserService.isAdmin(request) == False:
        raise exception_response(404)
    else :
        data = request.json_body    
        tour = Tour()
        tour.id     = data['id']
        tour.uid    = data['uid']
        tour = TourService.update_by_id_uid(tour.id, tour.uid, request=request)
        tour.status  = '2'
        tour.mtime  = datetime.datetime.now()
    return Response(
        '',
        headers=[
            ('X-Relocate', ''),
            ('Content-Type', 'text/html'),
        ]
    )

#Admin/Tour admin enable their tour. 
@view_config(route_name='admin_action', match_param='action=tour_enable')
def admin_tour_enable(request):
    print("ADMIN ENABLE TOUR")
    user = request.user
    
    #check only admin/tour admin access this function
    if user is None or UserService.isAdmin(request) == False:
        raise exception_response(404)
    else :
        data = request.json_body    
        tour = Tour()
        tour.id     = data['id']
        tour.uid    = data['uid']
        tour = TourService.update_by_id_uid(tour.id, tour.uid, request=request)
        tour.status  = '1'
        tour.mtime  = datetime.datetime.now()
    return Response(
        '',
        headers=[
            ('X-Relocate', ''),
            ('Content-Type', 'text/html'),
        ]
    )

#Admin/Tour admin delete their tour. 
@view_config(route_name='admin_action', match_param='action=tour_delete')
def admin_tour_delete(request):
    print("ADMIN DELETE TOUR")
    user = request.user
    
    #check only admin/tour admin access this function
    if user is None or UserService.isAdmin(request) == False:
        raise exception_response(404)
    else :
        data = request.json_body    
        tour = Tour()
        tour.id     = data['id']
        tour.uid    = data['uid']
        tour = TourService.update_by_id_uid(tour.id, tour.uid, request=request)
        tour.status  = '3'
        tour.mtime  = datetime.datetime.now()
    return Response(
        '',
        headers=[
            ('X-Relocate', ''),
            ('Content-Type', 'text/html'),
        ]
    )

#Admin/Tour admin delete their tour. 
@view_config(route_name='admin_action', match_param='action=tour_requestactive')
def admin_tour_requestactive(request):
    print("REQUEST ACTIVE TOUR")
    user = request.user
    
    #check only admin/tour admin access this function
    if user is None or UserService.isAdmin(request) == False:
        raise exception_response(404)
    else :
        data = request.json_body    
        tour = Tour()
        tour.id     = data['id']
        tour.uid    = data['uid']
        tour = TourService.update_by_id_uid(tour.id, tour.uid, request=request)
        tour.req_active  = '1'
        tour.mtime  = datetime.datetime.now()
    return Response(
        '',
        headers=[
            ('X-Relocate', ''),
            ('Content-Type', 'text/html'),
        ]
    )

#Admin active tour. 
@view_config(route_name='admin_action', match_param='action=tour_active')
def admin_tour_active(request):
    print("ADMIN ACTIVE TOUR")
    user = request.user
    
    #check only admin can access this function
    if user is None or UserService.isAdmin_2(request) == False:
        raise exception_response(404)
    else :
        data = request.json_body    
        tour = Tour()
        tour.id     = data['id']
        tour.uid    = data['uid']
        tour = TourService.update_by_id_uid(tour.id, tour.uid, request=request)
        tour.status  = '1'
        tour.mtime  = datetime.datetime.now()
    return Response(
        '',
        headers=[
            ('X-Relocate', ''),
            ('Content-Type', 'text/html'),
        ]
    )

#Admin restore tour. 
@view_config(route_name='admin_action', match_param='action=tour_restore')
def admin_tour_restore(request):
    print("ADMIN RESTORE TOUR")
    user = request.user
    
    #check only admin can access this function
    if user is None or UserService.isAdmin_2(request) == False:
        raise exception_response(404)
    else :
        data = request.json_body    
        tour = Tour()
        tour.id     = data['id']
        tour.uid    = data['uid']
        tour = TourService.update_by_id_uid(tour.id, tour.uid, request=request)
        tour.status  = '0'
        tour.mtime  = datetime.datetime.now()
    return Response(
        '',
        headers=[
            ('X-Relocate', ''),
            ('Content-Type', 'text/html'),
        ]
    )
