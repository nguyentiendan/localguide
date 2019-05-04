from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from .models import User
from .services.user_service import UserService

class UserAuthenticationPolicy(AuthTktAuthenticationPolicy):
    def authenticated_userid(self, request):
        user = request.user
        if user is not None:
            return user.uid

def get_user(request):
    uid = request.unauthenticated_userid
    if uid is not None:
        '''user = request.dbsession.query(User).get(uid)'''
        user = UserService.by_uid(uid, request=request)
        return user

def includeme(config):
    settings = config.get_settings()
    authn_policy = UserAuthenticationPolicy(
        settings['auth.secret'],
        hashalg='sha512',
    )
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(ACLAuthorizationPolicy())
    config.add_request_method(get_user, 'user', reify=True)
    