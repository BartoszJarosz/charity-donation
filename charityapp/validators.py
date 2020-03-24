from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def ValidateEmail(value):
    u = User.objects.filter(email=value)
    if u:
        raise ValidationError("Email jest już zajęty!")
