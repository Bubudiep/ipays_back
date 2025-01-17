# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'user', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth-info/', AuthInfo.as_view(), name='auth-info'),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
]
