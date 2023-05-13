from .models import users
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend

class Email_Backend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = users.objects.get(
                Q(username__iexact=username) |
                Q(email__iexact=username)
            )

        except users.DoesNotExist:
            return None

        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user(self, user_id):
        try:
            user = users.objects.get(pk=user_id)
        except users.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None
