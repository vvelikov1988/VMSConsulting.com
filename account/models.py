from uuid import uuid4
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin, UnicodeUsernameValidator
)
from django.utils.translation import ugettext_lazy as _
from django.core.validators import FileExtensionValidator
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail

from stdimage.models import StdImageField
from stdimage.validators import MinSizeValidator, MaxSizeValidator
from django_countries.fields import CountryField

from .model_addon import UploadToPathAndRename

USERNAME_VALIDATOR = UnicodeUsernameValidator()


class AccountManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('Account must have an email address'))
        if not username:
            raise ValueError(_('Account must have an username'))

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **extra_fields
        )
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_supervisor', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError(_('Superuser must have is_admin=True.'))
        if extra_fields.get('is_active') is not True:
            raise ValueError(_('Superuser must have is_active=True.'))
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_stuff=True.'))
        if extra_fields.get('is_supervisor') is not True:
            raise ValueError(_('Superuser must have is_supervisor=True.'))

        return self.create_user(
            username=username,
            email=self.normalize_email(email),
            password=password,
            **extra_fields
        )


class Account(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        verbose_name=_('Username'),
        max_length=100,
        unique=True,
        validators=[USERNAME_VALIDATOR],
        help_text=_('Required. 100 characters or fewer. Letters, digits and @/ ./+ /- /_ only. e.g. Adam_99')
    )
    email = models.EmailField(
        verbose_name=_('Email'),
        max_length=200,
        unique=True,
        help_text=_('Email: e.g. example@domain.com')
    )
    first_name = models.CharField(
        verbose_name=_('First Name'),
        max_length=100
    )
    last_name = models.CharField(
        verbose_name=_('Last Name'),
        max_length=100
    )

    profile_pic = StdImageField(
        verbose_name=_('Profile Image'),
        default='default/img/profile.png',
        upload_to=UploadToPathAndRename('upload/img/profile'),
        validators=[
            FileExtensionValidator(['png', 'jpg', 'jpeg']),
            MinSizeValidator(200, 200),
            MaxSizeValidator(1200, 1200)
        ],
        variations={
            'thumbnail': (40, 40, True),
            'medium': (200, 200, True),
            'large': (525, 525, True),
        }
    )

    country = CountryField(
        verbose_name=_('Country'),
        blank_label=_('__Select Country__')
    )

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_supervisor = models.BooleanField(default=False)
    is_team = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)

    global_token = models.CharField(max_length=255, default=uuid4)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    objects = AccountManager()

    class Meta:
        verbose_name = _('account')
        verbose_name_plural = _('accounts')

    def __str__(self):
        return ('%s' % self.username).strip()

    def get_full_name(self):
        return ('%s %s' % (self.first_name, self.last_name)).strip()

    def get_short_name(self):
        return ('%s' % self.first_name).strip()

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


WORK_TAGS_CHOICES = (
    (1, 'Front End'),
    (2, 'Back End'),
    (3, 'Full Stack'),
    (4, 'Designer'),
    (5, 'Leader'),
)


class TeamAccount(models.Model):
    account = models.ForeignKey(Account, related_name='team', on_delete=models.CASCADE)
    work_tag = models.IntegerField(
        verbose_name=_('Work Tag'),
        choices=WORK_TAGS_CHOICES
    )
    information = models.TextField()
    resume = models.FileField(
        verbose_name=_('Resume'),
        upload_to=UploadToPathAndRename('upload/resume'),
        validators=[
            FileExtensionValidator(['pdf', 'doc', 'docx']),
        ],
    )

    class Meta:
        verbose_name = _('team member')
        verbose_name_plural = _('team members')

    def __str__(self):
        return ('%s' % self.account.get_full_name()).strip()

    def get_topic_str(self):
        return WORK_TAGS_CHOICES[self.work_tag - 1][1]


class UserAccount(models.Model):
    account = models.ForeignKey(Account, related_name='user', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return ('%s' % self.account.get_full_name()).strip()
