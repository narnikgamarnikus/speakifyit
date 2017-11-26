import ujson as json
from celery import shared_task
from .models import ContactRequest, User


@shared_task
def create_contact_request(**kwargs):
	print(kwargs)
	to_user = get_object_or_None(User, pk=kwargs['to_user'])
	ContactRequest.objects.create(
		request_from = kwargs['from_user'],
		request_to = to_user
		)