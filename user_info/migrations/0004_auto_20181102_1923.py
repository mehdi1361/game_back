# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-02 15:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_info', '0003_message_read'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'پروفایل', 'verbose_name_plural': 'پروفایل ها'},
        ),
    ]