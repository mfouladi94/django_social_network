import uuid

from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, UserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_name = models.CharField(_('user name'), max_length=50 , unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(_('name'), max_length=255, blank=True, default='')
    avatar = models.ImageField(_('avatar'), upload_to='avatars', blank=True, null=True)

    friends = models.ManyToManyField('self', verbose_name=_('friends'), )
    friends_count = models.IntegerField(default=0, verbose_name=_('Number of friends'))

    posts_count = models.IntegerField(default=0, verbose_name=_('Number of posts'))

    is_active = models.BooleanField(default=True, verbose_name=_('is active'))
    is_superuser = models.BooleanField(default=False, verbose_name=_('is super user'), )
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now, verbose_name=_('time of joining'))
    last_login = models.DateTimeField(blank=True, null=True, verbose_name=_('last login '))

    USERNAME_FIELD = 'user_name'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
