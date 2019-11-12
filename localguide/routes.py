def includeme(config):
    config.add_static_view('static', 'static/assets', cache_max_age=3600)
    config.add_static_view('adstatic', 'static/adassets', cache_max_age=3600)
    
    #Routing for frontend page
    config.add_route('index', '/')
    config.add_route('publish_tour', 'publish_tour')
    config.add_route('blog', 'blog')
    config.add_route('auth_action', '/auth/{action}')
    config.add_route('user_action', '/user/{action}')
    config.add_route('tour_action', '/tour/{action}')
    config.add_route('orders_action', '/orders/{action}')
    config.add_route('post_action', '/post/{action}')
    config.add_route('common_action', '/common/{action}')

    #Routing for admin page
    config.add_route('admin_action', '/admin/{action}')
    config.add_route('admin_user_action', '/admin/user/{action}')
    config.add_route('admin_tour_action', '/admin/tour/{action}')
    
    #config.add_route('guide_detail', '/guide/{uid:\d+}')


