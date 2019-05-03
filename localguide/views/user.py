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
from ..services.user_service import UserService
from ..utils import XssHtml
import smtplib
#For send mail
from pyramid_mailer.message import Message
from pyramid_mailer.mailer import Mailer
from pyramid_mailer import get_mailer

@view_config(route_name='user_action', match_param='action=create', renderer='localguide:templates/front/user_create.jinja2')
def signup(request):
    print('USER CREATE')  
    user = User()
    
    if request.method == 'POST':
        data = request.json_body
        user.fullname    = data['fullname']
        user.email       = data['email']
        password         = data['password']
        user.set_password(password)
        user.random_uid()
        
        try :
            request.dbsession.add(user)
            settings = request.registry.settings
            access_rights = 0o755    
            user_folder = settings['user.folder'] + user.random_uid()
            os.mkdir(user_folder)
        except DBAPIError:
            return Response(db_err_msg, content_type='text/plain', status=500)
    return {}   

    '''
    mailer = get_mailer(request)
    message = Message(subject="hello world",
                sender="admin@mysite.com",
                recipients=["tiendanvn@gmail.com"],
                body="hello, arthur")
    mailer.send(message)
    '''

@view_config(route_name='user_action', match_param='action=basic', renderer='localguide:templates/user/basic_info.jinja2')
def user_basic(request):
    print('USER BASIC INFO')
    uid = request.unauthenticated_userid 
    User = UserService.by_uid(uid, request)
    
    if User is None :
        raise exception_response(404)
    if UserService.check_login(request) == False:
        raise exception_response(404)
    return dict(user=User)

    #if (not User) or (UserService.check_two_uid(uid, request) == False):
    #    raise exception_response(404)
    
@view_config(route_name='user_action', match_param='action=advance', renderer='localguide:templates/user/advance_info.jinja2')
def user_advance(request):
    print('USER ADVANCE INFO')
    uid = request.unauthenticated_userid 
    User = UserService.by_uid(uid, request)
    
    if User is None :
        raise exception_response(404)
    if UserService.check_login(request) == False:
        raise exception_response(404)
    return dict(user=User)



@view_config(route_name='user_action', match_param='action=updateBasicInfo')
def guide_updateBasicInfo(request):
    print("UPDATE BASIC INFO")
    
    uid = request.unauthenticated_userid
    if uid is None:
        raise exception_response(404)
    else:
        next_url = "/user/setting"
        data = request.json_body    
        user = User()
        user = UserService.by_uid(uid, request=request)
        user.fullname       = data['fullname']
        user.job            = data['job']
        user.mobile         = data['mobile']
        user.country        = data['country']
        user.city           = data['city']
        user.age            = data['age']
        user.sex            = data['sex']
        user.language       = data['language']
        user.hobby          = data['hobby']
        
        return Response(
                '',
                headers=[
                    ('X-Relocate', next_url),
                    ('Content-Type', 'text/html'),
                ]
        )

@view_config(route_name='user_action', match_param='action=updateExperience')
def guide_updateExperience(request):
    print("UPDATE Experience")
    
    uid = request.unauthenticated_userid     
    if uid is None:
        raise exception_response(404)
    else:
        next_url = "/guide/detail"
        data = request.json_body    
        user = User()
        user = UserService.by_uid(uid, request=request)

        #Xss process
        x = XssHtml.XssHtml()
        x.feed(data['experience'])
        x.close()
        data['experience'] = x.getHtml()

        user.experience		= data['experience']
        
        return Response(
                '',
                headers=[
                    ('X-Relocate', next_url),
                    ('Content-Type', 'text/html'),
                ]
        )

@view_config(route_name='user_action', match_param='action=updateWorkHistory')
def guide_updateWorkHistory(request):
    print("Update Work History")
    
    uid = request.unauthenticated_userid
    if uid is None:
        raise exception_response(404)
    else:
        next_url = "/guide/detail"
        data = request.json_body    
        user = User()
        user = UserService.by_uid(uid, request=request)

        #Xss process
        x = XssHtml.XssHtml()
        x.feed(data['work_history'])
        x.close()
        data['work_history'] = x.getHtml()

        user.work_history   = data['work_history']
        
        return Response(
                '',
                headers=[
                    ('X-Relocate', next_url),
                    ('Content-Type', 'text/html'),
                ]
        )
@view_config(route_name='guide_action', match_param='action=getRandomGuide', renderer='json')
def tour_getRandomGuide(request):
    print("GET RANDOM Guide")
    
    user = User()
    rs = UserService.get_RandomGuide(request=request)
    return [
        dict(id=user.id, uid=user.uid, fullname=user.fullname, avatar=user.avatar, country=user.country, city=user.city, job=user.job, language=user.language)
        for user in rs
    ]    

#Upload avatar of user
@view_config(route_name='user_action', match_param='action=uploadImage')
def guide_uploadImage(request):
    print("UPLOAD IMAGE")

    uid = request.unauthenticated_userid
    if uid is None:
        raise exception_response(404)
    else:
        user = User()
        user = UserService.by_uid(uid, request)

        if UserService.check_login(request) == False:
            raise exception_response(404)
        
        #if (not user) or (UserService.check_two_uid(uid, request) == False):
        #    raise exception_response(404)

        filename = request.POST['photo'].filename
        f, ext = os.path.splitext(filename)

        #setting new file name
        newFile = 'avatar' + ext
        
        # ``input_file`` contains the actual file data which needs to be
        # stored somewhere.
        input_file = request.POST['photo'].file

        #Check size here if you need (but size is checking by Vue)
        input_file.seek(0, 2) # Seek to the end of the file
        size = input_file.tell() # Get the position of EOF
        input_file.seek(0) # Reset the file position to the beginning
        
        #cwd = os.getcwd()
        #dir_path = os.path.dirname(os.path.realpath(__file__))

        settings = request.registry.settings
        user_folder = settings['user.folder'] + uid
        file_path = os.path.join(user_folder, '%s' % newFile)

        #file_path = os.path.join(cwd +'/localsearch/static/assets/user_img', '%s' % newFile)

        # We first write to a temporary file to prevent incomplete files from
        # being used.
        temp_file_path = file_path + '~'
        
        # Finally write the data to a temporary file
        input_file.seek(0)
        with open(temp_file_path, 'wb') as output_file:
            shutil.copyfileobj(input_file, output_file)

        # Now that we know the file has been fully saved to disk move it into place.
        moveFile = os.rename(temp_file_path, file_path)

        #Update guide avatar
        user.avatar = newFile

        return Response(
            '',
            headers=[
                ('X-Relocate', 'guide/detail'),
                ('Content-Type', 'text/html'),
            ]
        )

@view_config(route_name='guide_action', match_param='action=profile', renderer='localguide:templates/front/guide_profile.jinja2')
def user_profile(request):
    print('GUIDE PROFILE')
    id  = request.params.get('id')
    uid = request.params.get('hash')
    if id is None or uid is None :
        raise exception_response(404)
    else :
        user = User()
        user = UserService.by_id_uid(id, uid, request=request)
        if user is None :
            raise exception_response(404)

    return {'user':user}
