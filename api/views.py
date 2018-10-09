import uuid
import random

from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters, mixins
from rest_framework.permissions import AllowAny

from rest_framework.decorators import list_route
from rest_framework.response import Response

from common.payment import FactoryStore
from user_info.models import Profile

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, ProfileSerializer, ShopSerializer, GameSerializer, GameUserSerializer
from common.utils import Inline
from user_info.models import Device, Verification, GameUser, Message
from system.models import Shop, Store, PurchaseLog, Game
from django.conf import settings


def mobile_verified():
    def decorator(drf_custom_method):
        def _decorator(self, *args, **kwargs):
            if Profile.is_active(self.request.user):
                return drf_custom_method(self, *args, **kwargs)
            else:
                return Response({'id': 400, 'message': 'mobile not verified'},
                                status=status.HTTP_400_BAD_REQUEST
                                )

        return _decorator

    return decorator


def check_profile():
    def decorator(drf_custom_method):
        def _decorator(self, *args, **kwargs):

            # if Profile.is_active(self.request.user):
            if self.request.user.profile.name is None or \
                    self.request.user.profile.first_name is None or self.request.user.profile.last_name is None:

                return Response(
                    {
                        'id': 400,
                        'message': 'profile not complete'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                return drf_custom_method(self, *args, **kwargs)

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
            device_id = request.data.get('deviceUniqueID')
            device_name = request.data.get('deviceName')

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
    def set_profile(self, request):
        try:
            name = request.data.get('name')
            class_num = request.data.get('class_num')
            first_name = request.data.get('first_name')
            last_name = request.data.get('last_name')

            if name is None:
                raise Exception('name not found')

            if class_num is None:
                raise Exception('class_num not found')

            if first_name is None:
                raise Exception('first_name not found')

            if last_name is None:
                raise Exception('last_name not found')

            user_profile = Profile.objects.filter(name=name)

            if user_profile.count() > 0:
                name = '{}{}'.format(name.encode('utf-8'), str(uuid.uuid1().int >> 5))[:18]

            profile = Profile.objects.get(user=request.user)
            profile.name = name
            profile.first_name = first_name
            profile.last_name = last_name
            profile.save()

            return Response({'id': 201, 'user_name': name}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'id': 400, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

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
    @mobile_verified()
    def active_game(self, request):
        try:
            game_id = request.data.get('game_id')

            if game_id is None:
                raise Exception('game_id not found')

            game = Game.objects.get(id=game_id)

            if game.active_gem > request.user.profile.gem:
                raise Exception('not enough gem')

            game_serializer = GameSerializer(game)

            game_user = GameUser.objects.get(profile=request.user.profile, game=game)

            if game_user.active:
                raise Exception("game already unlock!!!")

            game_user.active = True
            game_user.save()

            request.user.profile.gem -= game.active_gem
            request.user.profile.save()

            return Response(
                {'id': 200,
                 'message':
                     {
                         "current_gem": request.user.profile.gem,
                         "used_gem": game.active_gem,
                         "game_unlock": game_serializer.data
                     }
                 },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response({'id': 400, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'])
    def set_mobile_number(self, request):
        mobile_no = request.data.get('mobile_no')

        if mobile_no is None:
            return Response({'id': 400, 'message': 'mobile number not found'}, status=status.HTTP_400_BAD_REQUEST)

        verification_code = random.randint(1000, 9999)

        try:
            user_profile = Profile.objects.get(mobile_number=mobile_no)

        except Exception as e:
            user_profile = Profile.objects.get(user=request.user)
            user_profile.mobile_number = mobile_no

        finally:
            user_profile.active = False
            user_profile.save()
            inline = Inline(mobile_nu=mobile_no, message=verification_code)
            result = inline.run()

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

    @list_route(methods=['POST'])
    @mobile_verified()
    @check_profile()
    def player_info(self, request):
        try:
            game_id = request.data.get('game_id')

            if game_id is None:
                raise Exception('game_id not found')

            game = Game.objects.get(id=game_id)
            game_serializer = GameSerializer(game)

            serializer = self.serializer_class(request.user.profile)
            result = serializer.data

            result['game'] = game_serializer.data

            game_user = GameUser.objects.get(profile=request.user.profile, game=game)
            game_user_serializer = GameUserSerializer(game_user)

            result['game-data'] = game_user_serializer.data

            return Response({'id': 200, 'message': result}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'id': 400, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'])
    @check_profile()
    def leader_board(self, request):
        try:
            game_id = request.data.get('game_id')

            if game_id is None:
                raise Exception('game_id not found')

            leader_board = GameUser.objects.filter(game_id=game_id, active=True).order_by('-score')
            serializer = GameUserSerializer(leader_board, many=True)
            result = []

            for index, item in enumerate(serializer.data):
                item['rank'] = index + 1
                result.append(item)

            return Response({'id': 200, 'message': result}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'id': 400, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'])
    @check_profile()
    def set_invitation_code(self, request):
        try:
            invitation_code_id = request.data.get('invitation_code')

            if invitation_code_id is None:
                raise Exception('inviter_code not found')

            inviter = GameUser.objects.get(profile__invitation_code=invitation_code_id)

            if request.user.profile.inviter_code is not None:
                raise Exception('inviter_code already exist')

            request.user.profile.invitation_code = inviter.profile.inviter_code
            request.user.profile.gem += settings.INVITE_REWARD
            request.user.profile.save()

            inviter.profile.gem += settings.INVITE_REWARD
            inviter.profile.save()

            serializer = ProfileSerializer(request.user.profile)

            Message.add(request.user.profile, 'invitation', 'invitation code accepted!!!')
            Message.add(inviter.profile, 'inviter', 'inviter code accepted!!!')

            return Response({'id': 200, 'message': serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'id': 400, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'])
    @check_profile()
    def game_result(self, request):
        try:
            game_id = request.data.get('game_id')
            level = request.data.get('level')

            if game_id is None:
                raise Exception('game_id not found')

            if level is None:
                raise Exception('level not found')

            if level not in ['level_1_reward', 'level_2_reward', 'level_2_reward']:
                raise Exception('reward not found')

        except Exception as e:
            return Response({'id': 400, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ShopViewSet(DefaultsMixin, AuthMixin, mixins.RetrieveModelMixin,
                  mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

    @list_route(methods=['POST'])
    @mobile_verified()
    def show(self, request):
        store_id = request.data.get('store_id')
        store = Store.objects.get(id=store_id)

        shop_items = Shop.objects.filter(active=True, store=store)
        serializer = self.serializer_class(shop_items, many=True)

        return Response({'id': 200, 'message': serializer.data}, status=status.HTTP_200_OK)

    @list_route(methods=['POST'])
    @mobile_verified()
    def buy(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
            shop = get_object_or_404(Shop, pk=request.data.get('shop_id'), enable=True)

            purchase_store = FactoryStore.create(
                shop=shop,
                purchase_token=request.data.get('purchase_token'),
                product_id=request.data.get('product_id'),
                package_name=request.data.get('package_name')
            )

            is_verified, message = purchase_store.is_verified()

            if not is_verified:
                PurchaseLog.objects.create(user=profile, store_purchase_token=request.data.get('purchase_token'),
                                           store_params=message, shop=shop)
                return Response({'id': 404, 'message': 'not found'}, status=status.HTTP_404_NOT_FOUND)

            PurchaseLog.objects.create(user=profile, store_purchase_token=request.data.get('purchase_token')
                                       , store_params=message, used_token=True, shop=shop)

            request.user.profile.gem += shop.quantity
            request.user.profile.save()

            return Response({'buy_gem': shop.quantity, 'user_gem': request.user.profile.gem},
                            status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            return Response({'id': 400, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
