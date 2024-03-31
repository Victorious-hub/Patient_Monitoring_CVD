from django.urls import path

from .apis import (
    NotificationCreateApi,
    NotificationListApi,
)

urlpatterns = [
    path('v1/<str:slug>/send', NotificationCreateApi.as_view(), name='send_notification'),
    path('v1/<str:slug>/patient', NotificationListApi.as_view(), name='list_notification')
]
