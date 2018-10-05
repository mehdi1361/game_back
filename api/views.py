import uuid
import random

from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import viewsets, status, filters, mixins
from rest_framework.permissions import AllowAny

from rest_framework.decorators import list_route
from rest_framework.response import Response
from user_info.models import Profile
from rest_framework.exceptions import PermissionDenied

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, ProfileSerializer
from common.utils import Kavenegar
from user_info.models import Device, Verification


def mobile_verified():
    def decorator(drf_custom_method):
        def _decorator(self, *args, **kwargs):
            if Profile.is_active(self.request.user):
                return drf_custom_method(self, *args, **kwargs)
            else:
                # raise PermissionDenied()
                return Response({'id': 400, 'message': 'mobile number not verified'},
                                status=status.HTTP_400_BAD_REQUEST
                                )
        return _decorator
    return decorator


class DefaultsMixin(object):
    paginate_by = 25
    paginate_by_param = 'page_size'
    max_paginate_by = 100
    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
)


class AuthMixin(object):
    authentication_classes = (
        TokenAuthentication,
        JSONWebTokenAuthentication
    )

    permission_classes = (
        IsAuthenticated,
    )


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (AllowAny,)

        return super(UserViewSet, self).get_permissions()

    def create(self, request, *args, **kwargs):
        try:
            device_id = request.data['deviceUniqueID']
            device_name = request.data['deviceName']

            player_id = str(uuid.uuid1().int >> 32)
            user = User.objects.create_user(username=player_id, password=player_id)
            Device.objects.create(device_id=device_id, device_name=device_name, user=user)

            return_id = 201

            return Response(
                {'id': return_id, 'player_id': player_id},
                status=status.HTTP_201_CREATED if return_id == 201 else status.HTTP_200_OK
            )

        except Exception as e:
            return Response({'id': 400, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(DefaultsMixin, AuthMixin, mixins.RetrieveModelMixin,
                     mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    @list_route(methods=['POST'])
    @mobile_verified()
    def set_player_name(self, request):
        name = request.data.get('name')
        user_profile = Profile.objects.filter(name=name)

        if user_profile.count() > 0:
            name = '{}{}'.format(name.encode('utf-8'), str(uuid.uuid1().int >> 5))[:18]

        profile, created = Profile.objects.get_or_create(user=request.user)
        profile.name = name
        profile.save()

        if created:
            return Response({'id': 201, 'user_name': name}, status=status.HTTP_201_CREATED)

        return Response({'id': 200, 'user_name': name}, status=status.HTTP_200_OK)

    @list_route(methods=['POST'])
    @mobile_verified()
    def change_player_name(self, request):
        if request.user.profile:
            name = request.data.get('name')
            user_profile = Profile.objects.filter(name=name)

            if user_profile.count() > 0:
                return Response({'id': 400, 'message': 'name already exists', 'name': name},
                                status=status.HTTP_400_BAD_REQUEST)

            profile = Profile.objects.get(user=request.user)
            profile.name = name
            profile.save()

            return Response({'id': 200, 'message': 'name changed', 'name': profile.name}, status=status.HTTP_200_OK)

        return Response({'id': 400, 'message': 'cant change name'}, status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'])
    def set_mobile_number(self, request):
        mobile_no = request.data.get('mobile_no')

        if mobile_no is None:
            return Response({'id': 400, 'message': 'mobile number not found'}, status=status.HTTP_400_BAD_REQUEST)

        verification_code = random.randint(1000, 9999)
        user_profile = None

        try:
            user_profile = Profile.objects.get(mobile_number=mobile_no)

        except Exception as e:
            user_profile = Profile.objects.get(user=request.user)
            user_profile.mobile_number = mobile_no

        finally:
            user_profile.active = False
            user_profile.save()
            kavenegar = Kavenegar(receptor=mobile_no, message=verification_code)
            result = kavenegar.run()

            if result:
                Verification.objects.create(
                    verification_code=verification_code,
                    profile=user_profile
                )

                return Response({'id': 200, 'message': 'verification code sent!!!'}, status=status.HTTP_200_OK)

        return Response({'id': 400, 'message': 'verification code send failed'}, status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'])
    def verified(self, request):
        response_id = 400
        state = status.HTTP_400_BAD_REQUEST

        verification_code = request.data.get('verification_code')
        verified, message = Verification.is_verified(user=request.user, verification_code=verification_code)

        if verified:
            profile = Profile.objects.get(user=request.user)
            profile.active = True
            profile.save()
            response_id = 200
            state = status.HTTP_200_OK

        return Response({'id': response_id, 'message': message}, status=state)



