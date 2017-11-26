from rest_framework import serializers, pagination
from .models import Message, Room
from rest_framework import serializers
from speakifyit.users.serializers import UserSerializer

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
