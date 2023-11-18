from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.signing import Signer
import uuid
# from django.utils import six

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + str(timestamp) +
            str(user.is_active)
        )

account_activation_token = TokenGenerator()
reset_token_signer = Signer()