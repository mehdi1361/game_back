# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-28 05:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0006_shop_shop_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaselog',
            name='used_token',
            field=models.BooleanField(default=False, verbose_name='used_token'),
        ),
    ]