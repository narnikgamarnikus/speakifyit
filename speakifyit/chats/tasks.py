import ujson as json
from celery import shared_task
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from annoying.functions import get_object_or_None
from .signals import create_message
from .models import Room, Notification
from speakifyit.users.models import ContactRequest
from channels import Group


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


@shared_task
def send_notification(**kwargs):
	notification = Notification.objects.create(
		from_user = kwargs['from_user'],
		to_user = kwargs['to_user'],
		msg_type = kwargs['msg_type'],
		content = kwargs['content'],
		icon = kwargs['icon'],
		link = kwargs['link']
		)

	# TODO:
	# 1. send WebSocket notification or subscribe from client to create Notification

@receiver(create_message, sender=Room)
def receiver_create_message(sender, *args, **kwargs):
	create_message_task.apply_async(kwargs=kwargs)


@receiver(post_save, sender=ContactRequest)
def send_requset_notification(sender, instance, created, **kwargs):
	if created:
		content = 'User {} wants to add you to the chat'.format(instanse.from_user)
		msg_type = 'create_request'
		from_user = instanse.from_user
		to_user = instanse.to_user

	elif instance.accepted is True:
		content = 'User {} wants to add you to the chat'.format(instanse.from_user),
		msg_type = 'create_request'
		from_user = instanse.to_user
		to_user = instanse.from_user

	elif instance.accepted is False:
		from_user = instanse.to_user
		to_user = instanse.from_user

	send_notification.apply_async(kwargs={
		'from_user': from_user,
		'to_user': to,
		'msg_type': msg_type,
		'content': content,
		'icon':'',
		'link':''
		})