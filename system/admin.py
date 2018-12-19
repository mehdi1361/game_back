from django.contrib import admin
from .models import SmsSender, Game, Store, Shop, ConfigFile


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
        'game_id',
        'bundle_version'
    ]

    list_editable = [
        'name',
        'active_gem',
        'level_1_complete_reward',
        'level_2_complete_reward',
        'level_3_complete_reward',
        'game_id',
        'bundle_version'
    ]


class ShopInline(admin.StackedInline):
    model = Shop


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'valid_name', 'access_token', 'refresh_token', 'store_id']
    list_editable = ['name', 'valid_name', 'access_token', 'refresh_token', 'store_id']
    inlines = [ShopInline, ]


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity', 'active', 'store', 'shop_id']
    list_editable = ['quantity', 'active', 'store', 'shop_id']


@admin.register(ConfigFile)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['id', 'file_config']
    list_editable = ['file_config', ]