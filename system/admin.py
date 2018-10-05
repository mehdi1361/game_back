from django.contrib import admin
from .models import SmsSender, Game


@admin.register(SmsSender)
class SmsSenderAdmin(admin.ModelAdmin):
    list_display = ['receptor', 'message', 'profile', 'status']


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['name']