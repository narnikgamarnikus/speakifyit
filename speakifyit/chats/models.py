from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils import timezone


@python_2_unicode_compatible
class Room(models.Model):

    users = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
    	return '-'.join(
    		user.username for user in self.users
    	)


@python_2_unicode_compatible
class Message(models.Model):

	room = models.ForeignKey(Room, related_name='messages')
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	timestamp = models.DateTimeField(db_index=True, default=timezone.now)
	content = models.TextField()

	def __str__(self):
		return '{0} at {1}'.format(self.user, self.timestamp)