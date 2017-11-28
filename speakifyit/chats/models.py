from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from channels import Group
from .settings import MSG_TYPE_MESSAGE, MESSAGE_TYPES_CHOICES
import ujson as json
from .signals import create_message
from django.utils import timezone
from model_utils.models import TimeStampedModel, SoftDeletableModel
from model_utils import FieldTracker


@python_2_unicode_compatible
class Base(SoftDeletableModel, TimeStampedModel):
	
	tracker = FieldTracker()

	class Meta:
		abstract = True


@python_2_unicode_compatible
class Room(Base):

	users = models.ManyToManyField(settings.AUTH_USER_MODEL)

	def __str__(self):
		return '-'.join(
			user.username for user in self.users
		)

	def clean(self):
		if self.users.count() > 2:
			raise ValidationError(_('The number of users in the room should not exceed 2.'))

	@property
	def websocket_group(self):
	    """
	    Returns the Channels Group that sockets should subscribe to to get sent
	    messages as they are generated.
	    """
	    return Group("room-%s" % self.id)

	def add_to_room(self, user, team_id, team_name, team_align):
		if not user in self.users.all():
			self.users.add(user)
			self.save()

	def leave_from_room(self, user, team_name, team_align):
		if user in self.users.all():
			self.users.delete(user)
			self.save()

	def send_message(self, message, user, msg_type=MSG_TYPE_MESSAGE):
		"""
		Called to send a message to the room on behalf of a user.
		"""
		final_msg = {
			'room_id': str(self.id), 'message': message, 
			'username': user.username, "timestamp": timezone.now().strftime('%I:%M:%S %p')
		}
		
		# Send signal for create new message
		create_message.send(
			sender=self.__class__, room=self.id, user=user, 
			msg_type=msg_type, content=message
			)

		# Send out the message to everyone in the room
		self.websocket_group.send(
		    {"text": json.dumps(final_msg)}
		)


@python_2_unicode_compatible
class Message(Base):

	room = models.ForeignKey(Room, related_name='messages')
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	#timestamp = models.DateTimeField(db_index=True, default=timezone.now)
	content = models.TextField()
	msg_type = models.PositiveSmallIntegerField(
		choices=MESSAGE_TYPES_CHOICES,
		default=MESSAGE_TYPES_CHOICES[0][0],
	)
	is_read = models.BooleanField(default=False)
	is_editable = models.BooleanField(default=True)

	@property
	def timestamp(self):
		return self.created.strftime('%I:%M:%S %p')

	def __str__(self):
		return '{0} at {1}'.format(self.user, self.timestamp)


class MessageChart(Base):
	
	message = models.ForeignKey(Message)
	approve_users = models.ManyToManyField(settings.AUTH_USER_MODEL)
	is_approved = models.BooleanField(default=False)

	def __str__(self):
		return str(self.pk) 


@python_2_unicode_compatible
class Notification(Base):

	TYPES = (
		('create_request', _('Create request')),
		('accept_request', _('Accept request')),
		('cancel_request', _('Cancel request')),
		('new_edited_message', _('New edited message'))
		)

	contact_request = models.ForeignKey('users.ContactRequest', null=True)
	msg_type = models.CharField(choices=TYPES, max_length=20)
	from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='from_user')
	to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='from_to')
	content = models.TextField()
	icon = models.TextField()
	link = models.URLField()
	is_read = models.BooleanField(default=False)

	def __str__(self):
		return str(self.pk)