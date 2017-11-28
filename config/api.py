from rest_framework import routers

from speakifyit.users.views import UserViewSet, ContactRequestViewSet

# Settings
api = routers.DefaultRouter()
api.trailing_slash = '/?'

# Users API
api.register(r'users', UserViewSet)
api.register(r'contact_request', ContactRequestViewSet)