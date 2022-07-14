from django.contrib.auth.models import AbstractUser
from django.db import models

from users.utils import CustomUserManager


class User(AbstractUser):
    # REQUIRED_FIELDS = ["name"]
    # USERNAME_FIELD = "username"
    objects = CustomUserManager()
