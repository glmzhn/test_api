from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import string
import random


def generate_unique_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


def generate_verification_code():
    return ''.join(random.choices(string.digits, k=4))


class User(models.Model):
    unique_id = models.CharField(max_length=6, unique=True, default=generate_unique_id)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    verif_code = models.CharField(max_length=4, null=False, blank=False, default=generate_verification_code)
    is_authenticated = models.BooleanField(default=False)
    code_created_at = models.DateTimeField(auto_now_add=True, null=True)
    invited_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='invited_users')
    has_invited = models.BooleanField(default=False)