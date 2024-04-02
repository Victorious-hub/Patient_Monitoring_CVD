from django.urls import path

from .apis import (
    NotificationListApi,
)

urlpatterns = [
    path('v1/<str:slug>/patient', NotificationListApi.as_view(), name='list_notification')
]
