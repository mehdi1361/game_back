# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-19 08:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0007_purchaselog_used_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='bundle_version',
            field=models.PositiveIntegerField(default=0, verbose_name='bundle version'),
        ),
    ]
