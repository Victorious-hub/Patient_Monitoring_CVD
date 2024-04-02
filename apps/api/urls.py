from django.urls import include, path

urlpatterns = [
    path('users/', include('apps.users.urls')),
    path('auth/', include('apps.authentication.urls')),
    path('analysis/', include('apps.analysis.urls')),
    path('notifications/', include('apps.notifications.urls')),
    path('treatment/', include('apps.treatment.urls')),
]