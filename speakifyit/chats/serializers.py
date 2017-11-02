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

'''
class EventSerializer(serializers.ModelSerializer):
	#event_messages = MessageSerializer(many=True)
	#messages = serializers.SerializerMethodField('event_messages')
	messages = serializers.HyperlinkedIdentityField(view_name='api_v1:event_messages_list')
	home_team = TeamSerializer()
	away_team = TeamSerializer()
	in_room = serializers.SerializerMethodField('check_user')

	def check_user(self, obj):
		user = self.context['request'].user
		return user in obj.users.all()

	class Meta:
	    model = Event
	    fields = ('id', 'status', 'name', 'home_team', 'away_team', 'messages', 'data', 'in_room')
'''