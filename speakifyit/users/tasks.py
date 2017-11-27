import ujson as json
from celery import shared_task
from .models import ContactRequest, User
from annoying.functions import get_object_or_None


@shared_task
def create_contact_request(**kwargs):
	to_user = get_object_or_None(User, pk=kwargs['to_user'])
	if to_user:
		contact_requset = ContactRequest.objects.create(
			request_from = kwargs['from_user'],
			request_to = to_user
		)
