from pyramid.httpexceptions import HTTPFound
from pyramid.security import (
    remember,
    forget,
    )
from pyramid.view import (
    forbidden_view_config,
    view_config,
)
from pyramid.response import Response
from ..models import User
from ..services.user_service import UserService

@view_config(route_name='auth_action', match_param='action=login', renderer='localguide:templates/front/login.jinja2')
def login(request):
    print('LOGIN')
    '''
    next_url = request.params.get('next', request.referrer)    
    if not next_url:
        next_url = request.route_url('index')
    message = ''
    email = ''
    ''' 
    user = request.user
    if user is not None :
        #have loging before
        return HTTPFound(location='/')  
    else :
        if request.method == 'POST' :
            data = request.json_body
            email       = data['email']
            password    = data['password']
            
            user = UserService.by_email(email, request)
            if user is not None and user.check_password(password) :
                headers = remember(request, user.uid)
                message = 'success'
                return Response(message, headers=headers, content_type='text/plain') 
                #return HTTPFound(location=next_url, headers=headers)
            else :
                message = 'Email or password is wrong.'            
                return Response(message, content_type='text/plain') 
        return {}

@view_config(route_name='auth_action', match_param='action=logout', renderer='json')
def logout(request):
    headers = forget(request)
    next_url = request.route_url('index')
    return HTTPFound(location=next_url, headers=headers)

@forbidden_view_config()
def forbidden_view(request):
    next_url = request.route_url('login', _query={'next': request.url})
    return HTTPFound(location=next_url)