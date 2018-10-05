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

    class Meta:
        db_table = 'game'
        verbose_name = _('game')
        verbose_name_plural = _('games')

    def __str__(self):
        return '{}'.format(self.name)
