from django.contrib import admin
from .models import SmsSender, Game, Store, Shop


@admin.register(SmsSender)
class SmsSenderAdmin(admin.ModelAdmin):
    list_display = ['receptor', 'message', 'profile', 'status']


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'active_gem',
        'level_1_complete_reward',
        'level_2_complete_reward',
        'level_3_complete_reward',
        'game_active_price'
    ]

    list_editable = [
        'name',
        'active_gem',
        'level_1_complete_reward',
        'level_2_complete_reward',
        'level_3_complete_reward',
        'game_active_price'
    ]


class ShopInline(admin.StackedInline):
    model = Shop


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['name', 'valid_name', 'access_token', 'refresh_token']
    list_editable = ['valid_name', 'access_token', 'refresh_token']
    inlines = [ShopInline, ]


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity', 'active', 'store']
    list_editable = ['quantity', 'active', 'store']
