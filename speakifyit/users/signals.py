from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from .models import User, ContactRequest

@receiver(post_save, sender=ContactRequest)
def request_contact(sender, instance, created, *args, **kwargs):
	if instance.accepted:
		instance.request_to.contacts.add(instance.request_from)
		instance.request_to.save()
		