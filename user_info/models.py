from django.db import models
from base.models import Base
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from datetime import datetime
from system.models import Game
from django.db.models import signals
import pytz


class Profile(Base):
    name = models.CharField(_('name'), max_length=200, null=True, blank=True)
    class_num = models.IntegerField(_('class'), null=True, blank=True)
    inviter_code = models.CharField(_('inviter code'), max_length=200, null=True, blank=True)
    gem = models.IntegerField(_('gem'), default=0, blank=True)
    mobile_number = models.CharField(_('mobile number'), max_length=15, null=True, blank=True, unique=True)
    active = models.BooleanField(_('active'), default=False)
    user = models.OneToOneField(User, verbose_name=_('profile'))

    class Meta:
        db_table = 'profiles'
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    def __str__(self):
        return '{}-{}'.format(self.name, self.user.username)

    @classmethod
    def is_active(cls, user):
        try:
            profile = cls.objects.get(user=user)
            return profile.active
        except:
            return False


class Device(Base):
    device_name = models.CharField(_('device name'), max_length=200, blank=True)
    device_id = models.CharField(_('device id'), max_length=200, blank=True)
    user = models.ForeignKey(User, verbose_name=_('profile'), related_name='devices', null=True, blank=True)

    class Meta:
        db_table = 'devices'
        verbose_name = _('device')
        verbose_name_plural = _('devices')
        unique_together = ('user', 'device_id')

    def __str__(self):
        return '{}-{}'.format(self.device_id, self.device_name)


class Verification(Base):
    verification_code = models.CharField(_('verification code'), max_length=8, blank=True)
    profile = models.ForeignKey(Profile, verbose_name=_('profile'), related_name='devices')

    class Meta:
        db_table = 'verification'
        verbose_name = _('verification')
        verbose_name_plural = _('verification')

    def __str__(self):
        return '{}-{}'.format(self.profile.mobile_number, self.verification_code)

    @classmethod
    def is_verified(cls, user, verification_code):
        try:
            profile = Profile.objects.get(user=user)
            verification = cls.objects.get(verification_code=verification_code, profile=profile)

            delta = datetime.now(tz=pytz.utc) - verification.created_date
            minute, seconds = divmod(delta.days * 86400 + delta.seconds, 60)
            if minute == 0 and seconds < 60:
                return True, 'verification code accepted'

            return False, 'verification code not accepted'

        except:
            return False, 'profile or verification code not found'


# class GameUser(Base):
#     profile = models.ForeignKey(Profile)


def create_user_dependency(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, gem=100)


signals.post_save.connect(create_user_dependency, sender=User)
