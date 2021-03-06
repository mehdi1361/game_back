# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-09 06:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_info', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='created date')),
                ('subject', models.CharField(max_length=200, verbose_name='subject')),
                ('body', models.TextField(verbose_name='body')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='user_info.Profile', verbose_name='profile')),
            ],
            options={
                'verbose_name': 'message',
                'verbose_name_plural': 'messages',
                'db_table': 'message',
            },
        ),
        migrations.AlterModelOptions(
            name='usercurrencylog',
            options={'verbose_name': 'user_currency', 'verbose_name_plural': 'user_currencies'},
        ),
        migrations.AlterModelTable(
            name='usercurrencylog',
            table='user_currency',
        ),
    ]
