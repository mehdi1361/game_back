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
    receptor = models.CharField(_('receptor'), max_length=20)
    message = models.TextField(_('message'), blank=True)
    profile = models.ForeignKey(User, verbose_name=_('profile'), related_name='verification_messages')
    status = models.CharField(_('status'), max_length=10, choices=STATUS, default='queued')

    class Meta:
        db_table = 'sms_sender'
        verbose_name = _('sms_sender')
        verbose_name_plural = _('sms_senders')

    def __str__(self):
        return '{}'.format(self.receptor)


class Game(Base):
    name = models.CharField(_('name'), max_length=50)
    active_gem = models.PositiveIntegerField(_('active gem'), default=10)
    level_1_complete_reward = models.PositiveIntegerField(_('level 1 complete reward'), default=10)
    level_2_complete_reward = models.PositiveIntegerField(_('level 2 complete reward'), default=20)
    level_3_complete_reward = models.PositiveIntegerField(_('level 3 complete reward'), default=30)
    game_active_price = models.PositiveIntegerField(_('level 3 complete reward'), default=30)

    class Meta:
        db_table = 'game'
        verbose_name = _('game')
        verbose_name_plural = _('games')

    def __str__(self):
        return '{}'.format(self.name)


class Store(Base):
    name = models.CharField(_('store name'), max_length=50)
    valid_name = models.CharField(_('valid name'), max_length=50, null=True, blank=True)
    access_token = models.CharField(_('access token'), max_length=50, null=True, blank=True)
    refresh_token = models.CharField(_('refresh token'), max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = _('store')
        verbose_name_plural = _('stores')
        db_table = 'stores'

    def __str__(self):
        return '{}'.format(self.name)


class Shop(Base):
    name = models.CharField(_('name'), max_length=50)
    quantity = models.PositiveIntegerField(_('quantity'), default=10)
    price = models.PositiveIntegerField(_('price'), default=10)
    active = models.BooleanField(_('active'), default=False)
    store = models.ForeignKey(Store, verbose_name=_('store'), null=True)

    class Meta:
        db_table = 'shop'
        verbose_name = _('shop')
        verbose_name_plural = _('shops')

    def __str__(self):
        return '{}'.format(self.name)


class PurchaseLog(Base):
    user = models.ForeignKey(User, verbose_name=_('profile'), related_name='purchase_logs')
    store_purchase_token = models.CharField(_('store purchase token'), max_length=100)
    store_params = models.CharField(_('store params'), max_length=100)
    shop = models.ForeignKey(Shop, verbose_name=_('shop'), related_name='users')

    class Meta:
        db_table = 'purchase_log'
        verbose_name = _('purchase_log')
        verbose_name_plural = _('purchase_logs')

    def __str__(self):
        return '{}'.format(self.store_purchase_token)