from rest_framework import serializers
from .models import Message, Room, Notification
from speakifyit.users.serializers import UserSerializer, ContactRequestSerializer

class RoomSerializer(serializers.ModelSerializer):
	users = UserSerializer(many=True)
	messages = serializers.HyperlinkedIdentityField(view_name='api:messages')

	class Meta:
		model = Room
		fields = ('id', 'users')


class MessageSerializer(serializers.ModelSerializer):

	class Meta:
		model = Message
		fields = ('id', 'user', 'msg_type', 'content', 'timestamp', 'created', 'modifed')


class NotificationSerializer(serializers.ModelSerializer):
	from_user = UserSerializer()
	to_user = UserSerializer()
	contact_request = ContactRequestSerializer()


	class Meta:
		model = Notification
		fields = '__all__'