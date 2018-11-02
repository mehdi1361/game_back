# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-02 16:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_info', '0004_auto_20181102_1923'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='device',
            options={'verbose_name': 'دستگاه', 'verbose_name_plural': 'دستگاه ها'},
        ),
        migrations.AlterModelOptions(
            name='gameuser',
            options={'verbose_name': 'بازی کاربر', 'verbose_name_plural': 'بازی کاربران'},
        ),
        migrations.AlterModelOptions(
            name='usercurrencylog',
            options={'verbose_name': 'اطلاعات کاربر', 'verbose_name_plural': 'اطلاعات کاربران'},
        ),
        migrations.AlterModelOptions(
            name='verification',
            options={'verbose_name': 'کد تایید', 'verbose_name_plural': 'کد تایید ها'},
        ),
        migrations.AlterField(
            model_name='device',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='devices', to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
        migrations.AlterField(
            model_name='gameuser',
            name='active',
            field=models.BooleanField(default=False, verbose_name='فعال'),
        ),
        migrations.AlterField(
            model_name='gameuser',
            name='game',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='system.Game', verbose_name='بازی'),
        ),
        migrations.AlterField(
            model_name='gameuser',
            name='invite_code',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='کد دعوت'),
        ),
        migrations.AlterField(
            model_name='gameuser',
            name='level_1_reward',
            field=models.BooleanField(default=False, verbose_name='جایزه مرحله اول'),
        ),
        migrations.AlterField(
            model_name='gameuser',
            name='level_2_reward',
            field=models.BooleanField(default=False, verbose_name='جایزه مرحله دوم'),
        ),
        migrations.AlterField(
            model_name='gameuser',
            name='level_3_reward',
            field=models.BooleanField(default=False, verbose_name='جایزه مرحله سوم'),
        ),
        migrations.AlterField(
            model_name='gameuser',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='games', to='user_info.Profile', verbose_name='کاربر'),
        ),
        migrations.AlterField(
            model_name='gameuser',
            name='score',
            field=models.PositiveIntegerField(default=0, verbose_name='امتیاز'),
        ),
        migrations.AlterField(
            model_name='gameuser',
            name='star',
            field=models.PositiveIntegerField(default=0, verbose_name='ستاره'),
        ),
        migrations.AlterField(
            model_name='message',
            name='body',
            field=models.TextField(verbose_name='شرح'),
        ),
        migrations.AlterField(
            model_name='message',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='user_info.Profile', verbose_name='کاربر'),
        ),
        migrations.AlterField(
            model_name='message',
            name='read',
            field=models.BooleanField(default=False, verbose_name='خوانده'),
        ),
        migrations.AlterField(
            model_name='message',
            name='subject',
            field=models.CharField(max_length=200, verbose_name='موضوع'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='active',
            field=models.BooleanField(default=False, verbose_name='فعال'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='class_num',
            field=models.IntegerField(blank=True, null=True, verbose_name='کلاس'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='first_name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='نام'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gem',
            field=models.IntegerField(blank=True, default=0, verbose_name='الماس'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='invitation_code',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='کد دعوت کننده'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='inviter_code',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='کد دعوت'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='last_name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='نام خانوادگی'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='mobile_number',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True, verbose_name='شماره موبایل'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='نام'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
        migrations.AlterField(
            model_name='usercurrencylog',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='usercurrencylog',
            name='gem',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='الماس'),
        ),
        migrations.AlterField(
            model_name='usercurrencylog',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='currency_logs', to='user_info.Profile', verbose_name='کاربر'),
        ),
        migrations.AlterField(
            model_name='usercurrencylog',
            name='used_in',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='استفاده شده در'),
        ),
        migrations.AlterField(
            model_name='verification',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='devices', to='user_info.Profile', verbose_name='پروفایل'),
        ),
        migrations.AlterField(
            model_name='verification',
            name='verification_code',
            field=models.CharField(blank=True, max_length=8, verbose_name='کد تایید'),
        ),
    ]
