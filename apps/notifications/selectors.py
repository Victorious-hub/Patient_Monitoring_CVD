from django.db import transaction
from typing import Iterable

from django.shortcuts import get_object_or_404

from apps.notifications.models import Notification
from apps.users.models import PatientProfile


class NotificationSelector:
    @transaction.atomic
    def list(self, slug) -> Iterable[Notification]:
        patient = get_object_or_404(PatientProfile, slug=slug)
        notifications = Notification.objects.filter(patient=patient)
        return notifications
