from rest_framework import routers

from speakifyit.users.views import UserViewSet, ContactRequestViewSet
from speakifyit.chats.views import NotificationViewSet

# Settings
api = routers.DefaultRouter()
api.trailing_slash = '/?'

# Users API
api.register(r'users', UserViewSet)
api.register(r'contact_requests', ContactRequestViewSet)
api.register(r'notifications', NotificationViewSet)