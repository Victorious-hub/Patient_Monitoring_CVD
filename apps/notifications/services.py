
from apps.users.models import PatientProfile


class NotificationService:
    def __init__(self,
                 patient: PatientProfile = None,
                 message: str = None,
                 is_read: bool = None,
                 slug: str = None,
                 ):
        self.patient = patient
        self.message = message
        self.is_read = is_read
        self.slug = slug
