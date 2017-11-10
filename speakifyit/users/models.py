from model_utils.models import TimeStampedModel, SoftDeletableModel
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from model_utils import FieldTracker
from django.db import models
from model_utils.fields import StatusField
from model_utils import Choices
from uuid import uuid4

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

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
    middle_name = models.CharField(_('Middle name'), blank=True, max_length=255)
    native = models.ManyToManyField(Language, related_name="native_languages")
    learn = models.ManyToManyField(Language, related_name="learn_languages")
    avatar = models.ImageField(
        upload_to=user_directory_path, 
        verbose_name=_('Avatar'), 
        blank=True
        )
    #gender = StatusField(choices_name=GENDERS)
    gender = models.CharField(
        choices=GENDERS, 
        default=GENDERS.male,
        max_length=6
    )
    token = models.UUIDField(verbose_name=_('Token'), default=uuid4, editable=False)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)
    full_name.fget.short_description = _('Full name')

    @property
    def short_name(self):
        return '{} {}{}'.format(self.last_name,
                                self.first_name[0] + '.' if self.first_name else '',
                                self.middle_name[0] + '.' if self.middle_name else '')

    def get_short_name(self):
        return self.short_name

    def get_full_name(self):
        return self.full_name