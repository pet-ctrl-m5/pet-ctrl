from django.contrib.auth.models import AbstractUser
from django.db import models

from users.utils import CustomUserManager


class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_manager = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    email = None
    REQUIRED_FIELDS = ["first_name", "last_name"]
    USERNAME_FIELD = "username"
    objects = CustomUserManager()
