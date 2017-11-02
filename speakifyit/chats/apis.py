from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .serializers import MessageSerializer, RoomSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .models import (
    Room, 
    Message
)


class RoomsApiListView(generics.ListAPIView):

	def get_queryset(self):
	    return Room.objects.filter(users__in=[self.request.user]).order_by('created')

	authentication_classes = (SessionAuthentication, BasicAuthentication)
	permission_classes = (IsAuthenticated,)
	serializer_class = MessageSerializer

class MessagesApiListView(generics.ListAPIView):

	def get_queryset(self):
		return Message.objects.filter(room=self.kwargs['pk']).order_by('created')

	serializer_class = MessageSerializer
	authentication_classes = (SessionAuthentication, BasicAuthentication)
	permission_classes = (IsAuthenticated,)	