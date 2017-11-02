from model_utils.models import TimeStampedModel, SoftDeletableModel
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from model_utils import FieldTracker
from django.db import models
from model_utils.fields import StatusField
from model_utils import Choices


@python_2_unicode_compatible
class Base(SoftDeletableModel, TimeStampedModel):
	
	tracker = FieldTracker()

	class Meta:
		abstract = True



@python_2_unicode_compatible
class Language(Base):

    language = models.CharField(max_length=50)
    flag = models.ImageField()

    def __str__(self):
    	return self.language


@python_2_unicode_compatible
class User(AbstractUser):

    GENDERS = Choices(
        ('male', 'male', _('Male')), 
        ('female', 'female', _('Female')),
        ('any', 'any', _('Any'))
    )

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_('Name of User'), blank=True, max_length=255)
    native = models.ManyToManyField(Language, related_name="native_languages")
    learn = models.ManyToManyField(Language, related_name="learn_languages")
    #gender = StatusField(choices_name=GENDERS)
    gender = models.CharField(
        choices=GENDERS, 
        default=GENDERS.male,
        max_length=6
    )

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})
