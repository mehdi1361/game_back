from django.contrib import admin
from .models import Profile, Device, GameUser, UserCurrencyLog


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'first_name',
        'last_name',
        'class_num',
        'inviter_code',
        'gem',
        'mobile_number',
        'active',
        'user',
        'invitation_code'
    ]


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = [
        'device_name',
        'device_id',
        'user'
    ]


@admin.register(GameUser)
class GameUserAdmin(admin.ModelAdmin):
    list_filter = ['game']

    list_display = [
        'profile',
        'game',
        'score',
        'star',
        'active',
        'invite_code',
        'level_1_reward',
        'level_2_reward',
        'level_3_reward'
    ]

    ordering = ['-score']


@admin.register(UserCurrencyLog)
class UserCurrencyLog(admin.ModelAdmin):
    list_display = [
        'profile',
        'gem',
        'used_in',
        'description'
    ]