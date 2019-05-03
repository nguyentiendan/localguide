from docutils.core import publish_parts
#from sqlalchemy.sql import select, and_, or_
from pyramid.response import Response
from pyramid.httpexceptions import exception_response
#from pyramid.security import (remember, forget,)
from pyramid.view import (forbidden_view_config, view_config,)
import os, uuid, shutil, random, string, json, datetime
import urllib.request
#from pyramid.httpexceptions import HTTPFound, HTTPNotFound,  HTTPForbidden
#from ..models.tour import Tour
#from ..models.user import User
from ..services.user_service import UserService
#from ..services.tour_service import TourService


@view_config(route_name='common_action', match_param='action=uploadEditorImage', renderer='json')
def quill_uploadImage(request):
    print("QUILL UPLOAD IMAGE")
    
    if UserService.check_login(request) == False :
        raise exception_response(404)
    else :
        uid = request.unauthenticated_userid
        filename = request.POST['photo'].filename
        f, ext = os.path.splitext(filename)

        #setting new file name
        rd = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(16)])
        newFile = uid + '_' + rd + ext
        
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
        host = settings['host']
        user_folder = settings['user.folder'] + uid
        file_path = os.path.join(user_folder, '%s' % newFile)
        
        # We first write to a temporary file to prevent incomplete files from
        # being used.
        temp_file_path = file_path + '~'
        
        # Finally write the data to a temporary file
        input_file.seek(0)
        with open(temp_file_path, 'wb') as output_file:
            shutil.copyfileobj(input_file, output_file)

        # Now that we know the file has been fully saved to disk move it into place.
        os.rename(temp_file_path, file_path)

        url = host + 'static/user_images/guide/' + uid + '/' + newFile
        return {'url': url}
