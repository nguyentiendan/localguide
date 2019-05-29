from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.include('.models')
    config.include('.routes')
    config.include('.security')
    config.include('pyramid_mailer')
    config.add_jinja2_search_path("templates")
    config.scan('.views')
    #config.scan()
    
    return config.make_wsgi_app()
