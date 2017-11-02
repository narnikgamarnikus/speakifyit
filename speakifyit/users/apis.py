from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from rest_framework import generics
from .models import User


class UsersApiDetailView(generics.RetrieveAPIView):

	serializer_class = UserSerializer
	authentication_classes = (SessionAuthentication, BasicAuthentication)
	permission_classes = (IsAuthenticated,)


class UsersNativeApiListView(generics.ListAPIView):

	def get_queryset(self):
		return User.objects.filter(native__in=[native for native in self.request.user.native.all()])

	serializer_class = UserSerializer
	authentication_classes = (SessionAuthentication, BasicAuthentication)
	permission_classes = (IsAuthenticated,)


class UsersLearnApiListView(generics.ListAPIView):

	def get_queryset(self):
		return User.objects.filter(learn__in=[learn for learn in self.request.user.learn.all()])

	serializer_class = UserSerializer
	authentication_classes = (SessionAuthentication, BasicAuthentication)
	permission_classes = (IsAuthenticated,)
