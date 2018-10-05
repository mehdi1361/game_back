from django.contrib.auth import get_user_model
from rest_framework import serializers
from user_info.models import Profile


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
        model = get_user_model()
        fields = (
            'id',
            'name',
            'class_num',
            'gem',
            'mobile_number',
            'active'
        )
