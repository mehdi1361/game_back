# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-29 05:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0012_auto_20181223_1521'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='bundle_version',
            new_name='update_step',
        ),
    ]