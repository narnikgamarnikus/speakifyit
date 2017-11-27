from functools import wraps
from .exceptions import ClientError
from annoying.functions import get_object_or_None
from channels.sessions import channel_session
from speakifyit.users.models import User
from django.core.cache import cache
import ujson as json


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
            if not message.user is user:
                message.user = user
        return func(message, *args, **kwargs)

    return inner


def message_text_token_user(func):

    @channel_session
    @wraps(func)
    def inner(message, *args, **kwargs):
        if 'token' in message['text']:
            token = json.loads(message['text'])['token']
            user = cache.get(token)
            if not user:
                user = get_object_or_None(User, token=token)
                cache.set(user.token, user)
            message.user = user
        else:
            raise ValueError('Token was not set in the message')
        return func(message, *args, **kwargs)

    return inner


def message_content_token_user(func):

    @channel_session
    @wraps(func)
    def inner(message, *args, **kwargs):
        if 'token' in message.content:
            token = message.content['token']
            user = cache.get(token)
            if not user:
                user = get_object_or_None(User, token=token)
                cache.set(user.token, user)
            message.user = user        
        else:
            raise ValueError('Token was not set in the message')
        return func(message, *args, **kwargs) 

    return inner