# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-06 06:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0007_auto_20181006_0950'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='params',
        ),
        migrations.RemoveField(
            model_name='smssender',
            name='params',
        ),
    ]
