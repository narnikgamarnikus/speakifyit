import ujson as json
from celery import shared_task
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from annoying.functions import get_object_or_None
from .signals import create_message
from .models import Room

@shared_task
def create_message_task(**kwargs):

	if kwargs['msg_type'] == 4:
		content = '{} joined the room'.format(kwargs['user'].username)
	elif kwargs['msg_type'] == 5:
		content = '{} left the room'.format(kwargs['user'].username)		

	if not content:
		content = kwargs['content']

	room = get_object_or_None(Room, kwargs['room'])

	if room:
		msg = Message.objects.create(
			user = kwargs['user'], content = content, msg_type = kwargs['msg_type'] 
		)
		print('message was created')

@receiver(create_message, sender=Room)
def receiver_create_message(sender, *args, **kwargs):
	create_message_task.apply_async(kwargs=kwargs)