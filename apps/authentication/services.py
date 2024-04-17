from django.db import transaction
from apps.users.models import CustomUser


class AuthService:
    def __init__(self,
                 email: str = None
                 ):
        self.email = email

    @transaction.atomic
    def get_role(self):
        user = CustomUser.objects.get(email=self.email)
        return user.role
