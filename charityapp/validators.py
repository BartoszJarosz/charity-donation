import re

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def validate_email(value):
    u = User.objects.filter(email=value)
    if u:
        raise ValidationError("Email jest już zajęty!")


def validate_password(value):
    if len(value) < 8 or \
            not re.search(r'\W', value) or \
            not re.search(r'\d', value) or \
            not re.search(r'[a-z]', value) or \
            not re.search(r'[A-Z]', value):
        raise ValidationError(
            "Hasło musi posiadać przynajmniej jeden znak specjalny, jedną cyfrę, dużą i małą litere!")
