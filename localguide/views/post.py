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
from ..models.post import Post
from ..services.user_service import UserService
from ..services.tour_service import TourService
from ..services.post_service import PostService
from ..utils import XssHtml


@view_config(route_name='blog', renderer='../templates/front/blog.jinja2')
def blog(request):
    print('ALL POST')
    post = PostService.front_postall(request=request)
    print(post)
    return {'post':post}

@view_config(route_name='post_action', match_param='action=create')
def post_create(request):
    print('POST CREATE')
    user = request.user
    #After create, Should be send mail to admin

    #check only admin access this function
    if user is None or UserService.isAdmin(request) == False:
        raise exception_response(404)
    else :
        post = Post()
        role = request.user.role        
        if request.method == 'POST':
            post.uid        = request.user.uid       
            post.title      = request.POST['title']
            post.content    = request.POST['content'].replace("'", "\\'" )

            try :
                request.dbsession.add(post)
                next_url = 'postlist'
                return Response(
                        next_url,
                        headers=[
                            ('X-Relocate', next_url),
                            ('Content-Type', 'text/html'),
                        ]
                )
            except DBAPIError:
                return Response(db_err_msg, content_type='text/plain', status=500)  
        return {}

@view_config(route_name='post_action', match_param='action=updatePost')
def post_update(request):
    print("UPDATE POST")
    #After update, Should be send mail to admin

    user = request.user
    #check only admin access this function
    if user is None or UserService.isAdmin(request) == False:
        raise exception_response(404)
    else :
        post = Post()
        if request.method == 'POST':
            data = request.json_body    
            post = PostService.by_id_uid(data['id'], request.user.uid, request=request)
            post.title       = data['title']
            post.content     = data['content'].replace("'", "\\'" )
            post.mtime       = datetime.datetime.now()   
            
        return Response(
                '',
                headers=[
                    ('X-Relocate', ''),
                    ('Content-Type', 'text/html'),
                ]
        )