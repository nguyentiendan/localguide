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
from ..utils import XssHtml
import stripe

@view_config(route_name='tour_action', match_param='action=all', renderer='localguide:templates/front/tour_all.jinja2')
def front_tourall(request):
    print('ALL TOUR')
    tour = TourService.front_tourall(request=request)
    
    return {'tour':tour}
    
@view_config(route_name='tour_action', match_param='action=detail', renderer='localguide:templates/tour/tour_detail.jinja2')
def tour_detail(request):
    print('TOUR DETAIL')
    id  = request.params.get('id')
    uid = request.params.get('hash')
    #user = request.user
    
    if id is None or uid is None :
        raise exception_response(404)
    else :
        tour = Tour()
        tour = TourService.detail_by_id_uid(id, uid, request=request)
        if tour is None :
            raise exception_response(404)
    return {'tour':tour}

@view_config(route_name='tour_action', match_param='action=charge')
def tour_charge(request):
    print('TOUR CHARGE')
    data = request.json_body
    id  = data['id']    #tourID
    uid  = data['uid']  #UserID
    token_id  = data['stripeToken']
    token_email  = data['stripeEmail']
    name_card = data['name_card']
    phone = data['phone']
    currency = data['currency']
    
    tour = Tour()
    tour = TourService.detail_by_id_uid(id, uid, request=request)

    if uid is None or id is None or tour is None or token_id is None:
        raise exception_response(404)
    else :
        stripe.api_key = 'sk_test_zhVLqm2IiBSzHCmYZbJwlwB400fY8QkLs2'
        try :
            charge = stripe.Charge.create (
                amount = str(tour.Tour.price) + '00',
                currency = currency,
                description = "Payment",
                source = token_id,
                capture = False,
                #statement_descriptor='Custom descriptor'
            )
        except Exception as e:
            return Response('Error', content_type='text/plain', status=500)  
        
        if charge.status == 'succeeded' :
            orders = Orders()
            orders.uid             = uid
            orders.tour_id         = id
            orders.tour_title      = tour.Tour.title
            orders.tour_price      = tour.Tour.price
            orders.tour_currency   = currency
            orders.charge_id       = charge.id
            orders.name_card       = name_card
            orders.email           = token_email
            orders.phone           = phone
            orders.status          = 'payment_succeeded'

            try :
                request.dbsession.add(orders)
            except DBAPIError:
                return Response(db_err_msg, content_type='text/plain', status=500)  
        
            return Response(
                    charge.status,
                    headers=[
                        ('X-Relocate', ''),
                        ('Content-Type', 'text/html'),
                    ]
            )
    
@view_config(route_name='tour_action', match_param='action=create')
def tour_create(request):
    print('TOUR CREATE')
    user = request.user
    #After create, Should be send mail to admin

    #check only admin access this function
    if user is None or UserService.isAdmin(request) == False:
        raise exception_response(404)
    else :
        tour = Tour()
        role = request.user.role        
        if request.method == 'POST':
            tour.uid        = request.user.uid       
            tour.title      = request.POST['title']
            tour.type       = request.POST['type']
            tour.short_desc = request.POST['short_desc']
            tour.country    = request.POST['country']
            tour.city       = request.POST['city']
            tour.price      = request.POST['price']
            tour.days       = request.POST['days']
            tour.content    = request.POST['content'].replace("'", "\\'" )
            if(request.POST['banner']!='undefined'):
                tour.banner = banner_upload(request.user.uid, request.POST['banner'], request)

            try :
                request.dbsession.add(tour)
                # Get the new ID and redirect
                t = request.dbsession.query(Tour.id).order_by(Tour.id.desc()).first()    
                # Create folder for tour
                settings = request.registry.settings
                tour_folder = settings['user.folder'] + request.user.uid + '/' + str(t.id)
                access_rights = 0o755    
                os.mkdir(tour_folder)
                next_url = 'uploadPhoto?id=' + str(t.id) + '&hash=' + request.user.uid 
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

@view_config(route_name='tour_action', match_param='action=updateTour')
def tour_update(request):
    print("UPDATE TOUR")
    #After update, Should be send mail to admin

    user = request.user
    #check only admin access this function
    if user is None or UserService.isAdmin(request) == False:
        raise exception_response(404)
    else :
        tour = Tour()
        if request.method == 'POST':
            data = request.json_body    
            tour = TourService.by_id_uid(data['id'], request.user.uid, request=request)
            tour.title       = data['title']
            tour.type        = data['type']
            tour.short_desc  = data['short_desc']
            tour.country     = data['country']
            tour.city        = data['city']
            tour.price       = data['price']
            tour.days        = data['days']
            tour.content     = data['content'].replace("'", "\\'" )
            tour.mtime       = datetime.datetime.now()   
        return Response(
                '',
                headers=[
                    ('X-Relocate', ''),
                    ('Content-Type', 'text/html'),
                ]
        )
@view_config(route_name='tour_action', match_param='action=deleteTour')
def tour_delete(request):
    print("DELETE TOUR")
    data = request.json_body
    id  = data['id']
    uid = data['uid']
    user = request.user

    if uid is None or id is None or user is None :
        raise exception_response(404)
    else :
        tour = Tour()
        tour = TourService.delete_id_uid(id, uid, request=request)
        return Response(
            '',
            headers=[
                ('X-Relocate', ''),
                ('Content-Type', 'text/html'),
            ]
        )        

@view_config(route_name='tour_action', match_param='action=disableTour')
def tour_disable(request):
    print("DISABLE TOUR")
    data = request.json_body
    id  = data['id']
    uid = data['uid']
    user = request.user

    if uid is None or id is None or uid != request.user.uid :
        raise exception_response(404)
    else :
        tour = Tour()
        tour = TourService.by_id_uid(id, uid, request=request)
        tour.status = '2'
        return Response(
                '',
                headers=[
                    ('X-Relocate', ''),
                    ('Content-Type', 'text/html'),
                ]
        )        

@view_config(route_name='tour_action', match_param='action=enableTour')
def tour_enable(request):
    print("ENABLE TOUR")
    data = request.json_body
    id  = data['id']
    uid = data['uid']
    user = request.user

    if uid is None or id is None or uid != request.user.uid :
        raise exception_response(404)
    else :
        tour = Tour()
        tour = TourService.by_id_uid(id, uid, request=request)
        tour.status = '1'
        return Response(
                '',
                headers=[
                    ('X-Relocate', ''),
                    ('Content-Type', 'text/html'),
                ]
        )        

#Upload banner when create new Tour
def banner_upload(uid,file,request):
    filename = file.filename
    f, ext = os.path.splitext(filename)

    #setting new file name
    newFile = 'banner_' + datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S") + ext
    
    # ``input_file`` contains the actual file data which needs to be
    # stored somewhere.
    input_file = file.file

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
    
    return newFile


@view_config(route_name='tour_action', match_param='action=getTourNotActive', renderer='json')
def tour_getTourNotActive(request):
    print("GET TOUR NOT ACTIVE")
    
    user = request.user     
    if user is None:
        raise exception_response(404)
    else:           
        tour = Tour()
        rs = TourService.get_TourNotActive(request.user.uid, request=request)
        return [
            dict(id=tour.id, uid=tour.uid, title=tour.title)
            for tour in rs
        ]

@view_config(route_name='tour_action', match_param='action=getTourActive', renderer='json')
def tour_getTourActive(request):
    print("GET TOUR ACTIVE")
    
    user = request.user     
    if user is None:
        raise exception_response(404)
    else:           
        tour = Tour()
        rs = TourService.get_TourActive(uid, request=request)
        return [
            dict(id=tour.id, uid=tour.uid, title=tour.title, status=tour.status)
            for tour in rs
        ]    

@view_config(route_name='tour_action', match_param='action=getRandomTour', renderer='json')
def tour_getRandomTour(request):
    print("GET RANDOM TOUR")    
    rs = TourService.get_RandomTour(request=request)
    return [
        dict(id=tour.id, uid=tour.uid, title=tour.title, type=tour.type, short_desc=tour.short_desc, price=tour.price, days=tour.days, banner=tour.banner)
        for tour in rs
    ]

@view_config(route_name='tour_action', match_param='action=getRelatedTour', renderer='json')
def tour_getRelatedTour(request):
    print("GET RELATED TOUR")
    id  = request.params.get('id')
    uid = request.params.get('uid')
    if uid is None or id is None :
        raise exception_response(404)
    else :
        rs = TourService.get_RelatedTour(uid, request=request)
        if rs is None :
            raise exception_response(404)
    return [
        dict(id=tour.id, uid=tour.uid, title=tour.title, type=tour.type, short_desc=tour.short_desc, price=tour.price, days=tour.days, banner=tour.banner)
        for tour in rs
    ]    

@view_config(route_name='tour_action', match_param='action=uploadTourPhoto')
def tour_uploadTourPhoto(request):
    print("UPLOAD TOUR PHOTO")
    
    id  = request.POST['id']
    uid = request.POST['uid']
    fileslist = request.POST.getall('photos')
    user = request.user

    #check only admin access this function
    if user is None or UserService.isAdmin(request) == False or uid != request.user.uid :
        raise exception_response(404)
    else:
        settings = request.registry.settings
        user_folder = settings['user.folder'] + request.user.uid + '/' + id
        photo_json = os.path.join(user_folder, '%s' % "photo.json")
        
        data = {}  
        data['images'] = []  

        for file in fileslist :
            #print ( "individual files: ", file.filename )
            f, ext = os.path.splitext(file.filename)
            
            # ``input_file`` contains the actual file data which needs to be
            # stored somewhere.
            input_file = file.file

            #Check size here if you need (but size is checking by Vue)
            input_file.seek(0, 2) # Seek to the end of the file
            size = input_file.tell() # Get the position of EOF
            input_file.seek(0) # Reset the file position to the beginning
            
            #cwd = os.getcwd()
            #dir_path = os.path.dirname(os.path.realpath(__file__))    
            file_path = os.path.join(user_folder, '%s' % file.filename)
            
            # We first write to a temporary file to prevent incomplete files from
            # being used.
            temp_file_path = file_path + '~'
            
            # Finally write the data to a temporary file
            #input_file.seek(0)
            with open(temp_file_path, 'wb') as output_file:
                shutil.copyfileobj(input_file, output_file)

            # Now that we know the file has been fully saved to disk move it into place.
            moveFile = os.rename(temp_file_path, file_path)
            
            data['images'].append({  
                'name': file.filename,
                'alt': 'copyright@localguide', 
            })
            with open(photo_json, "w") as json_file:
                json.dump(data, json_file)

        message = 'success'
        return Response(
            message,
            headers=[
                ('X-Relocate', ''),
                ('Content-Type', 'text/html'),
            ]
        )        

#Update banner when edit Tour
@view_config(route_name='tour_action', match_param='action=uploadImage')
def tour_uploadImage(request):
    print("UPLOAD IMAGE")
    
    id  = request.POST['id']
    hash = request.POST['hash']
    user = request.user
    #check only admin access this function
    if user is None or UserService.isAdmin(request) == False or hash != request.user.uid :
        raise exception_response(404)
    else:
        tour = Tour()
        tour = TourService.by_id_uid(id, request.user.uid, request=request)
        #user = UserService.by_uid(uid, request)

        #if UserService.check_login(request) == False:
        #    raise exception_response(404)
        
        #if (not user) or (UserService.check_two_uid(uid, request) == False):
        #    raise exception_response(404)

        filename = request.POST['photo'].filename
        f, ext = os.path.splitext(filename)

        #setting new file name
        newFile = 'banner_' + datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S") + ext
        
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
        user_folder = settings['user.folder'] + request.user.uid
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

        #Update banner
        tour.id     = id
        tour.uid    = request.user.uid
        tour.banner = newFile

        #try :
        #    request.dbsession.add(tour)
        #except DBAPIError:
        #    return Response(db_err_msg, content_type='text/plain', status=500)

        return Response(
            '',
            headers=[
                ('X-Relocate', ''),
                ('Content-Type', 'text/html'),
            ]
        )