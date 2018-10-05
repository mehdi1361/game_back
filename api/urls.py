from rest_framework.routers import DefaultRouter

from .views import UserViewSet, ProfileViewSet

router = DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'profile', ProfileViewSet)
