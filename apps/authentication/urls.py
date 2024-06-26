from django.urls import path
from apps.authentication.apis import ObtainTokenAPIView, UserLogoutAPi
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [

    path('v1/authenticate', ObtainTokenAPIView.as_view()),
    path('v1/token/refresh', TokenRefreshView.as_view()),
    path('v1/logout', UserLogoutAPi.as_view()),
]
