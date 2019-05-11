from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import (
    Authenticated,
    Everyone,
)

from .models import User
from .services.user_service import UserService

class UserAuthenticationPolicy(AuthTktAuthenticationPolicy):
    def authenticated_userid(self, request):
        user = request.user
        if user is not None:
            return user.uid

    def effective_principals(self, request):
        principals = [Authenticated]
        user = request.user
        if user is not None:
            #principals.append(Authenticated)
            principals.append(str(user.uid))
            principals.append(user.role)
            print(principals)
        return principals
    
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
    