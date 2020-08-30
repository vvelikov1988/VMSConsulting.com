from django.contrib.auth.backends import ModelBackend

import sys

from account.models import Account


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        """ Authenticate a user based on email address as the user name. """
        try:
            user = Account.objects.get(email=username)
            if user.check_password(password):
                return user
        except Account.DoesNotExist:
            try:
                user = Account.objects.get(username=username)
                if user.check_password(password):
                    return user
            except Account.DoesNotExist:
                Account().set_password(password)

    def get_user(self, user_id):
        """ Get a User object from the user_id. """
        try:
            return Account.objects.get(pk=user_id)
        except Account.DoesNotExist:
            return None