from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255,null=True)
    postal_code = models.PositiveIntegerField(null=True, blank=True)
    note = models.TextField(blank=True, null=True)
