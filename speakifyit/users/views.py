from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import User


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):

    fields = ['name', ]

    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter






import requests
from uuid import uuid4

from django.contrib.auth import authenticate, login
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from rest_framework import viewsets, status
from rest_framework.decorators import list_route
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer, UserWriteSerializer
from rest_framework import permissions

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return UserSerializer
        return UserWriteSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(self.request.data.get('password'))
        user.save()

    def perform_update(self, serializer):
        user = serializer.save()
        if self.request.data.get('password'):
            user.set_password(self.request.data.get('password'))
            user.save()

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    @list_route(methods=['GET'])
    def profile(self, request):
        if request.user.is_authenticated():
            serializer = self.serializer_class(request.user)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    @list_route(methods=['POST'], authentication_classes=[])
    def login(self, request, format=None):
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        user = authenticate(username=email, password=password)
        if user:
            login(request, user)
            return Response(status=status.HTTP_200_OK, data=user.token)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @list_route(methods=['POST'], authentication_classes=[])
    def register(self, request):
        last_name = request.data.get('last_name', None)
        first_name = request.data.get('first_name', None)
        middle_name = request.data.get('middle_name', None)
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        if User.objects.filter(email__iexact=email).exists():
            return Response({'status': 210})

        # user creation
        user = User.objects.create(email=email,
                                   password=password,
                                   last_name=last_name,
                                   first_name=first_name,
                                   middle_name=middle_name,
                                   is_admin=True)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

    @list_route(methods=['POST'])
    def password_reset(self, request, format=None):
        if User.objects.filter(email=request.data['email']).exists():
            user = User.objects.get(email=request.data['email'])
            send_mail(subject='Password reset',
                      message=render_to_string('mail/password_reset.txt', {'user': user, 'DOMAIN': settings.DOMAIN}),
                      from_email=settings.DEFAULT_FROM_EMAIL,
                      recipient_list=[request.data['email']])
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @list_route(methods=['POST'])
    def password_change(self, request, format=None):
        if User.objects.filter(token=request.data['token']).exists():
            user = User.objects.get(token=request.data['token'])
            user.set_password(request.data['password'])
            user.token = uuid4()
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @list_route(methods=['POST'])
    def validate_email(self, request):
        if settings.DJANGO_MAILGUN_API_PUB:
            response = requests.get(
                'https://api.mailgun.net/v3/address/validate',
                auth=('api', settings.DJANGO_MAILGUN_API_PUB),
                params={'address': request.data.get('email')})
            return Response(response.json())
        else:
            return Response({'is_valid': True})
