
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _
from django.db import models
from simple_history.models import HistoricalRecords
import uuid


# Create your models here.

class Base(models.Model):
    created_date = models.DateTimeField(_('created date'), auto_now_add=True)
    updated_date = models.DateTimeField(_('created date'), auto_now=True)
    # params = JSONField(_('params'), null=True, blank=True)

    class Meta:
        abstract = True
