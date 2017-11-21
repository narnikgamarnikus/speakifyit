from rest_framework import authentication
from rest_framework import exceptions
from django.contrib.auth import authenticate
from django.core.cache import cache
from speakifyit.users.models import User

class CustomTokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.GET.get('token')

        if not token:
            raise exceptions.AuthenticationFailed('No such token')       
       
        try:
            user = cache.get(token)
            if not user:
                user = User.objects.get(token=token)
                cache.set(token, user)
        except:
            raise exceptions.AuthenticationFailed('Authentication Failed')
        
        return (user, None)