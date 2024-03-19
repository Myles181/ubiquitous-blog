from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenRefreshView
)

urlpatterns = [
    path('', get_routes, name='get_routes'),
    path('token/', MyTokenObtainPairView.as_view(), name='token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('test/', protected_routes, name='test'),
    path('profile/', getProfile, name='get_profile'),
    path('profile/<int:id>/', updateProfile, name='update_profile'),
]

