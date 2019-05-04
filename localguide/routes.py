def includeme(config):
    config.add_static_view('static', 'static/assets', cache_max_age=3600)
    config.add_static_view('html', 'templates/static')
    config.add_route('index', '/')
    
    config.add_route('guide_action', '/guide/{action}')
    config.add_route('auth_action', '/auth/{action}')
    config.add_route('user_action', '/user/{action}')
    config.add_route('tour_action', '/tour/{action}')
    config.add_route('common_action', '/common/{action}')
    
    #config.add_route('guide_detail', '/guide/{uid:\d+}')


