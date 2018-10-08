import uuid

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
    first_name = models.CharField(_('first name'), max_length=200, null=True, blank=True)
    last_name = models.CharField(_('last name'), max_length=200, null=True, blank=True)
    class_num = models.IntegerField(_('class'), null=True, blank=True)
    inviter_code = models.CharField(_('inviter code'), max_length=200, null=True, blank=True)
    gem = models.IntegerField(_('gem'), default=0, blank=True)
    mobile_number = models.CharField(_('mobile number'), max_length=15, null=True, blank=True, unique=True)
    active = models.BooleanField(_('active'), default=False)
    user = models.OneToOneField(User, verbose_name=_('profile'))
    invitation_code = models.CharField(_('invitation code'), max_length=20, null=True, blank=True, unique=True)

    class Meta:
        db_table = 'profiles'
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    def __str__(self):
        return '{}-{}'.format(self.name, self.user.username)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.pk is None:
            self.inviter_code = str(uuid.uuid1().int >> 8)[:10]

        super(Profile, self).save(force_insert=False, force_update=False, using=None, update_fields=None)

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
            if minute <= 1 and seconds < 60:
                return True, 'verification code accepted'

            return False, 'verification code not accepted'

        except:
            return False, 'profile or verification code not found'


class GameUser(Base):
    profile = models.ForeignKey(Profile, verbose_name=_('profile'), related_name='games', null=True)
    game = models.ForeignKey(Game, verbose_name=_('profile'), related_name='users', null=True)
    score = models.PositiveIntegerField(_('score'), default=0)
    star = models.PositiveIntegerField(_('star'), default=0)
    active = models.BooleanField(_('active'), default=False)
    invite_code = models.CharField(_('invite code'), max_length=20, null=True, blank=True)
    level_1_reward = models.BooleanField(_('level 1 reward'), default=False)
    level_2_reward = models.BooleanField(_('level 2 reward'), default=False)
    level_3_reward = models.BooleanField(_('level 3 reward'), default=False)

    class Meta:
        db_table = 'game_user'
        verbose_name = _('game_user')
        verbose_name_plural = _('game_users')

    def __str__(self):
        return '{}-{}'.format(self.profile.name, self.game.name)

    @classmethod
    def set_invite_code(cls, profile, game, code):
        try:
            game_user = cls.objects.get(profile=profile, game=game)

            if code != profile.invitation_code:
                raise Exception('invitation code')

            game_user.invite_code = code
            game_user.save()

            return True, 'code accepted'
        except Exception as e:
            return False, str(e)

    @classmethod
    def is_active(cls, game_id, user):
        try:
            game_user = cls.objects.get(game_id=game_id, profile=user.profile)

            return game_user.active

        except Exception as e:
            return False, str(e)


class UserCurrencyLog(Base):
    profile = models.ForeignKey(Profile, verbose_name=_('profile'), related_name='currency_logs')
    gem = models.PositiveIntegerField(_('gem'), default=0, null=True, blank=True)
    used_in = models.CharField(_('used in'), max_length=100, null=True, blank=True)
    description = models.TextField(_('description'), null=True, blank=True)


def create_user_dependency(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance, gem=100)

        for game in Game.objects.all():
            GameUser.objects.create(profile=profile, game=game)


def create_game_user(sender, instance, created, **kwargs):
    if created:
        for user in User.objects.all():
            GameUser.objects.create(profile=user.profile, game=instance)


signals.post_save.connect(create_user_dependency, sender=User)
signals.post_save.connect(create_game_user, sender=Game)
