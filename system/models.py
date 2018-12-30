import os

from common.helper import OverwriteStorage
from django.db import models
from base.models import Base
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class QueuedManager(models.Manager):
    def get_queryset(self):
        return super(QueuedManager, self).get_queryset().filter(status='queued')


class SmsSender(Base):
    STATUS = (
        ('queued', 'queued'),
        ('sending', 'sending'),
        ('sent', 'sent'),
        ('failed', 'failed')
    )
    receptor = models.CharField(_('ارسال کننده'), max_length=20)
    message = models.TextField(_('پیام'), blank=True)
    profile = models.ForeignKey(User, verbose_name=_('کاربر'), related_name='verification_messages')
    status = models.CharField(_('وضعیت'), max_length=10, choices=STATUS, default='queued')

    class Meta:
        db_table = 'sms_sender'
        verbose_name = _('پیامک')
        verbose_name_plural = _('پیامک ها')

    def __str__(self):
        return '{}'.format(self.receptor)


class Game(Base):
    name = models.CharField(_('نام'), max_length=50)
    active_gem = models.PositiveIntegerField(_('الماس لازم برای فعالسازی'), default=10)
    level_1_complete_reward = models.PositiveIntegerField(_('جایزه مرحله اول'), default=10)
    level_2_complete_reward = models.PositiveIntegerField(_('جایزه مرحله دوم'), default=20)
    level_3_complete_reward = models.PositiveIntegerField(_('جایزه مرحله  سوم'), default=30)
    game_id = models.PositiveIntegerField(_('کد یکتای بازی'), null=True, blank=True, unique=True)
    update_step = models.PositiveIntegerField(_('update step'), default=0)

    class Meta:
        db_table = 'game'
        verbose_name = _('بازی')
        verbose_name_plural = _('بازیها')

    def __str__(self):
        return '{}'.format(self.name)


class Store(Base):
    name = models.CharField(_('نام فروشگاه'), max_length=50)
    valid_name = models.CharField(_('نام اصلی'), max_length=50, null=True, blank=True)
    access_token = models.CharField(_('توکن دسترسی'), max_length=50, null=True, blank=True)
    refresh_token = models.CharField(_('توکن نوسازی'), max_length=50, null=True, blank=True)
    store_id = models.PositiveIntegerField(_('کد یکتای فروشگاه'), null=True, blank=True, unique=True)

    class Meta:
        verbose_name = _('فروشگاه')
        verbose_name_plural = _('فروشگاهها')
        db_table = 'stores'

    def __str__(self):
        return '{}'.format(self.name)


class Shop(Base):
    name = models.CharField(_('نام'), max_length=50)
    quantity = models.PositiveIntegerField(_('تعداد'), default=10)
    price = models.PositiveIntegerField(_('قیمت'), default=10)
    active = models.BooleanField(_('فعال'), default=False)
    shop_id = models.PositiveIntegerField(_('کد یکتای پکیج'), null=True, blank=True, unique=True)
    store = models.ForeignKey(Store, verbose_name=_('فروشگاه'), null=True)

    class Meta:
        db_table = 'shop'
        verbose_name = _('پکیج')
        verbose_name_plural = _('پکیج ها')

    def __str__(self):
        return '{}'.format(self.name)


class PurchaseLog(Base):
    user = models.ForeignKey(User, verbose_name=_('profile'), related_name='purchase_logs')
    store_purchase_token = models.CharField(_('store purchase token'), max_length=100)
    store_params = models.CharField(_('store params'), max_length=100)
    shop = models.ForeignKey(Shop, verbose_name=_('shop'), related_name='users')
    used_token = models.BooleanField(_('used_token'), default=False)

    class Meta:
        db_table = 'purchase_log'
        verbose_name = _('اطلاعات مالی کاربر')
        verbose_name_plural = _('اطلاعات مالی کاربران')

    def __str__(self):
        return '{}'.format(self.store_purchase_token)


def image_path(instance, filename):
    return os.path.join('some_dir', str(instance.some_identifier), 'filename.ext')


class ConfigFile(Base):
    file_config = models.FileField(_('file config'), max_length=200, upload_to='config', null=True, storage=OverwriteStorage())

    class Meta:
        db_table = 'config_file'
        verbose_name = _('فایل کانفیگ')
        verbose_name_plural = _('فایل کانفیگ')

    def __str__(self):
        return '{}'.format(self.id)


class Reward(Base):
    inviter_reward = models.PositiveIntegerField(_('جایزه دعوت از دوستان'), default=100)
    register_reward = models.PositiveIntegerField(_('جایزه نصب بازی'), default=100)
    enable = models.BooleanField(_('فعال'), default=False)

    class Meta:
        db_table = 'reward_data'
        verbose_name = _('جوایز')
        verbose_name_plural = _('جوایز')

    def __str__(self):
        return '{}'.format(self.id)