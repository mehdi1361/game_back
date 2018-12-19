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
    YEAR_STATUS = (
        ('1397', '1397'),
        ('1398', '1398'),
        ('1399', '1399'),
        ('1400', '1400'),
        ('1401', '1401'),
        ('1402', '1402'),
        ('1403', '1403'),
        ('1404', '1404'),
        ('1405', '1405'),
        ('1405', '1405'),
        ('1406', '1406'),
        ('1407', '1407'),
        ('1408', '1408'),
        ('1409', '1409'),
        ('1410', '1410'),
    )
    name = models.CharField(_('نام'), max_length=200, null=True, blank=True)
    first_name = models.CharField(_('نام'), max_length=200, null=True, blank=True)
    last_name = models.CharField(_('نام خانوادگی'), max_length=200, null=True, blank=True)
    class_num = models.IntegerField(_('کلاس'), null=True, blank=True)
    inviter_code = models.CharField(_('کد دعوت'), max_length=200, null=True, blank=True)
    gem = models.IntegerField(_('الماس'), default=0, blank=True)
    mobile_number = models.CharField(_('شماره موبایل'), max_length=15, null=True, blank=True, unique=True)
    active = models.BooleanField(_('فعال'), default=False)
    user = models.OneToOneField(User, verbose_name=_('کاربر'), on_delete=models.CASCADE)
    invitation_code = models.CharField(_('کد دعوت کننده'), max_length=20, null=True, blank=True, unique=True)
    year = models.CharField(_('سال تحصیلی'), max_length=5, default='1397', choices=YEAR_STATUS)

    class Meta:
        db_table = 'profiles'
        verbose_name = _('پروفایل')
        verbose_name_plural = _('پروفایل ها')

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
    device_name = models.CharField(_('نام دستگاه'), max_length=200, blank=True)
    device_id = models.CharField(_('کد دستگاه'), max_length=200, blank=True)
    user = models.ForeignKey(User, verbose_name=_('کاربر'), related_name='devices', null=True, blank=True)

    class Meta:
        db_table = 'devices'
        verbose_name = _('دستگاه')
        verbose_name_plural = _('دستگاه ها')
        unique_together = ('user', 'device_id')

    def __str__(self):
        return '{}-{}'.format(self.device_id, self.device_name)


class Verification(Base):
    verification_code = models.CharField(_('کد تایید'), max_length=8, blank=True)
    profile = models.ForeignKey(Profile, verbose_name=_('پروفایل'), related_name='devices')

    class Meta:
        db_table = 'verification'
        verbose_name = _('کد تایید')
        verbose_name_plural = _('کد تایید ها')

    def __str__(self):
        return '{}-{}'.format(self.profile.mobile_number, self.verification_code)

    @classmethod
    def is_verified(cls, mobile_no, verification_code):
        try:
            verification = cls.objects.get(
                verification_code=verification_code,
                profile__mobile_number=mobile_no
            )

            delta = datetime.now(tz=pytz.utc) - verification.created_date
            minute, seconds = divmod(delta.days * 86400 + delta.seconds, 60)
            if minute <= 1 and seconds < 60:
                return True, 'verification code accepted', verification.profile.user.username

            return False, 'verification code not accepted', None

        except:
            return False, 'profile or verification code not found', None


class GameUser(Base):
    profile = models.ForeignKey(Profile, verbose_name=_('کاربر'), related_name='games', null=True)
    game = models.ForeignKey(Game, verbose_name=_('بازی'), related_name='users', null=True)
    score = models.PositiveIntegerField(_('امتیاز'), default=0)
    star = models.PositiveIntegerField(_('ستاره'), default=0)
    active = models.BooleanField(_('فعال'), default=False)
    invite_code = models.CharField(_('کد دعوت'), max_length=20, null=True, blank=True)
    level_1_reward = models.BooleanField(_('جایزه مرحله اول'), default=False)
    level_2_reward = models.BooleanField(_('جایزه مرحله دوم'), default=False)
    level_3_reward = models.BooleanField(_('جایزه مرحله سوم'), default=False)

    class Meta:
        db_table = 'game_user'
        verbose_name = _('بازی کاربر')
        verbose_name_plural = _('بازی کاربران')

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
    profile = models.ForeignKey(Profile, verbose_name=_('کاربر'), related_name='currency_logs')
    gem = models.PositiveIntegerField(_('الماس'), default=0, null=True, blank=True)
    used_in = models.CharField(_('استفاده شده در'), max_length=100, null=True, blank=True)
    description = models.TextField(_('توضیحات'), null=True, blank=True)

    class Meta:
        db_table = 'user_currency'
        verbose_name = _('اطلاعات کاربر')
        verbose_name_plural = _('اطلاعات کاربران')

    def __str__(self):
        return '{}-{}'.format(self.profile.name, self.gem)


class Message(Base):
    profile = models.ForeignKey(Profile, verbose_name=_('کاربر'), related_name='messages')
    read = models.BooleanField(_('خوانده'), default=False)
    subject = models.CharField(_('موضوع'), max_length=200)
    body = models.TextField(_('شرح'))

    class Meta:
        db_table = 'message'
        verbose_name = _('message')
        verbose_name_plural = _('messages')

    def __str__(self):
        return '{}-{}'.format(self.profile.name, self.subject)

    @classmethod
    def add(cls, profile, subject, body):
        try:
            cls.objects.create(profile=profile, subject=subject, body=body)
            return True

        except Exception as e:
            return False


def create_user_dependency(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance, gem=100)

        for game in Game.objects.all():
            GameUser.objects.create(profile=profile, game=game)


def create_game_user(sender, instance, created, **kwargs):
    if created:
        for user in User.objects.all():
            try:
                profile = Profile.objects.get(user=user)
                GameUser.objects.create(profile=user.profile, game=instance)

            except:
                pass


def delete_profile_user(sender, instance, **kwargs):
    try:
        user = User.objects.get(pk=instance.user.id)
        user.delete()

    except:
        pass


signals.post_save.connect(create_user_dependency, sender=User)
signals.post_save.connect(create_game_user, sender=Game)
signals.post_delete.connect(delete_profile_user, sender=Profile)
