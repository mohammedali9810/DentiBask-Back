# backends.py
from django.contrib.auth.backends import ModelBackend


class NoPasswordBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = super().authenticate(request, username=username, password=password, **kwargs)

        # If user is not found, create a user without checking the password
        if user is None:
            user = self.get_user(username)

        return user
