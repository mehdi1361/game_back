from django.contrib.auth import get_user_model
from rest_framework import serializers

from system.models import Shop, Game
from user_info.models import Profile, GameUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'username',
            'password'
        )


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = (
            'id',
            'name',
            'class_num',
            'gem',
            'mobile_number',
            'active',
            'inviter_code',
            'invitation_code',
            'year'
        )


class ShopSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shop
        fields = (
            'id',
            'name',
            'quantity',
            'price'
        )


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = (
            'id',
            'name',
            'level_1_complete_reward',
            'level_2_complete_reward',
            'level_3_complete_reward',
            'active_gem',
            'game_id',
            'bundle_version'
        )


class GameUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameUser

        fields = (
            'score',
            'star',
            'level_1_reward',
            'level_2_reward',
            'level_3_reward',
            'active'
        )
