from pyramid.response import Response
from pyramid.view import view_config


@view_config(route_name='index', renderer='../templates/front/index.jinja2')
def index(request):
    print('INDEX')
    return {}

@view_config(route_name='publish_tour', renderer='../templates/front/publish_tour.jinja2')
def publish(request):
    print('PUBLISH TOUR')
    return {}
