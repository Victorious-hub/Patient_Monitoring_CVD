from django.db import transaction
from typing import Iterable

from apps.notifications.models import Notification
from apps.users.models import PatientProfile
from apps.users.utils import get_object


class NotificationSelector:

    @transaction.atomic
    def notification_list(self, slug) -> Iterable[Notification]:
        patient = get_object(PatientProfile, slug=slug)
        notifications = Notification.objects.filter(patient=patient)
        for i in notifications:
            i.is_read = True
        return notifications
