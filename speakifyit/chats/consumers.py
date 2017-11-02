# In consumers.py
from channels import Group
from .models import Message, Room
import ujson as json
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http
from channels.security.websockets import allowed_hosts_only
from .utils import get_room_or_error, catch_client_error


@channel_session_user_from_http
def chat_connect(message):
	message.reply_channel.send({'accept': True})
	rooms = Room.objects.filter(users__in=[message.user])
	for room in rooms:
		#if message.user in room.users.all():
		room.websocket_group.add(message.reply_channel)
	message.channel_session['rooms'] = [room.id for room in rooms]


@channel_session_user
def chat_message(message):
	payload = json.loads(message['text'])
	payload['reply_channel'] = message.content['reply_channel']
	Channel("chat.receive").send(payload)


@channel_session_user
def chat_disconnect(message):
	# Unsubscribe from any connected rooms
	for room_id in message.channel_session.get("rooms", set()):
	    try:
	        room = Room.objects.get(pk=room_id)
	        # Removes us from the room's send group. If this doesn't get run,
	        # we'll get removed once our first reply message expires.
	        room.websocket_group.discard(message.reply_channel)
	    except Room.DoesNotExist:
	        pass


@channel_session_user
@catch_client_error
def chat_join(message):
	# Find the room they requested (by ID) and add ourselves to the send group
	# Note that, because of channel_session_user, we have a message.user
	# object that works just like request.user would. Security!
	room = get_room_or_error(message["user_id"], message.user)
	
	# Send a "enter message" to the room if available
	if NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
	    room.send_message(None, message.user, MSG_TYPE_ENTER)

	# OK, add them in. The websocket_group is what we'll send messages
	# to so that everyone in the chat room gets them.
	room.websocket_group.add(message.reply_channel)
	message.channel_session['rooms'] = list(set(message.channel_session['rooms']).union([room.id]))
	# Send a message back that will prompt them to open the room
	# Done server-side so that we could, for example, make people
	# join rooms automatically.

	room.add_to_room(message.user, team_id, team_name, team_align)

	message.reply_channel.send({
	    "text": json.dumps({
	        "join": str(room.id),
	        "timestamp": timezone.now().strftime('%I:%M:%S %p')
	    }),
	})


@channel_session_user
@catch_client_error
def chat_leave(message):
	# Reverse of join - remove them from everything.
	room = get_room_or_error(message["room"], message.user)

	# Send a "leave message" to the room if available
	if NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS:
	    room.send_message(None, message.user, MSG_TYPE_LEAVE)

	room.websocket_group.discard(message.reply_channel)
	message.channel_session['rooms'] = list(set(message.channel_session['rooms']).difference([room.id]))
	# Send a message back that will prompt them to close the room

	room.leave_from_room(message.user, team_name, team_align)

	message.reply_channel.send({
	    "text": json.dumps({
	        "leave": str(room.id),
	    }),
	})


@channel_session_user
@catch_client_error
def chat_send(message):
	# Check that the user in the room
	if int(message['room']) not in message.channel_session['rooms']:
	    raise ClientError("ROOM_ACCESS_DENIED")
	# Find the room they're sending to, check perms
	room = get_room_or_error(message["room"], message.user)
	# Send the message along
	room.send_message(message["message"], message.user)
