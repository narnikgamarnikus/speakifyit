from functools import wraps

from .exceptions import ClientError
from .models import Room
#from .models import Room
from annoying.functions import get_object_or_None
from django.core.cache import cache
#from rest_framework.authtoken.models import Token
from speakifyit.users.models import User
from channels.sessions import channel_session


def catch_client_error(func):
    """
    Decorator to catch the ClientError exception and translate it into a reply.
    """
    @wraps(func)
    def inner(message, *args, **kwargs):
        try:
            return func(message, *args, **kwargs)
        except ClientError as e:
            # If we catch a client error, tell it to send an error string
            # back to the client on their reply channel
            e.send_to(message.reply_channel)
    return inner


def get_room_or_error(room_id, user):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    # Check if the user is logged in
    if not user.is_authenticated():
        raise ClientError("USER_HAS_TO_LOGIN")
    # Find the room they requested (by ID)
    try:
        room = Room.objects.get(pk=room_id)
    except Room.DoesNotExist:
        raise ClientError("ROOM_INVALID")
    return room

def path_token(func):

    @channel_session
    @wraps(func)
    def inner(message, *args, **kwargs):
        
        from django.contrib.auth.models import AnonymousUser
        message.user = AnonymousUser()

        last_path_item = message.content['path'].split("/")[-1]
        split_last_item = last_path_item.split('=')
        
        if split_last_item.count('token') == 1:
            token = split_last_item[1]
            if token:
                message.token = token
            else:
                raise ValueError('Token was not set')
        elif split_last_item.count('token') > 1:
            raise ValueError('More than one token specified')
        else:
            raise ValueError('Token was not set in the path')
        
        return func(message, *args, **kwargs)

    return inner


def path_token_user(func):

    @path_token
    @wraps(func)
    def inner(message, *args, **kwargs):
        if hasattr(message, 'token'):
            token = message.token
            user = cache.get(token)
            if not user:
                user = get_object_or_None(User, token=token)
                cache.set(user.token, user)
            message.user = user
        return func(message, *args, **kwargs)

    return inner



def cookie_token(func):

    @wraps(func)
    def inner(message, *args, **kwargs):
        headers = message.get('headers')
        if headers:
            headers = dict(message['headers'])
            if b'token' in headers[b'cookie']:
                cookie = headers[b'cookie'].decode('utf-8')
                items = cookie.split(';')
                token = [item.split('=')[1] for item in items if item.split('=')[0] == ' token'][0]
                message.token = token
            else:
                from django.contrib.auth.models import AnonymousUser
                message.user = AnonymousUser()
                raise ValueError("Not found token in the cookie.")
        else:
            raise ValueError("Not found headers in the message.")
        
        return func(message, *args, **kwargs)
    return inner

def cookie_token_user(func):
    
    @cookie_token
    @wraps(func)
    def inner(message, *args, **kwargs):
        token = message.token
        user = cache.get(token)
        if not user:
            user = get_object_or_None(User, token=token)
            cache.set(user.token, user)
        message.user = user

        return func(message, *args, **kwargs)
    return inner


def check_token(message=None):
    if message:
        path = message.content['path'].split("/")[-1]
        if path.split('='):
            if path.split('=')[0] == 'token':
                user= get_object_or_None(User, token=path.split('=')[1])
    if not user:
        raise ClientError("USER_HAS_TO_LOGIN")
    else:
        set_user(user)
    return user.token


def get_user(message=None):
    user = None
    if message:
        try:
            print(message.content)
            path = message.content['path'].split("/")[0]
            if path.split('='):
                if path.split('=')[0] == 'token':
                    user = cache.get(path.split('=')[1])
        except:
            pass
        try:
            user = cache.get(message.content['token'])
        except:
            pass
    if not user:
        raise ClientError("USER_HAS_TO_LOGIN")
        
    return user


def set_user(user=None):
    if user:
        cache.set(user.token, user)
    return cache.get(user.token)