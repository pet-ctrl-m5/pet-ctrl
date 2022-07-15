from django.contrib.auth.models import AbstractUser
from django.db import models

from staffs.utils import CustomUserManager


class Staff(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_manager = models.BooleanField()
    is_doctor = models.BooleanField()
    is_staff = models.BooleanField()
    email = None
    REQUIRED_FIELDS = ["first_name", "last_name"]
    USERNAME_FIELD = "username"
    objects = CustomUserManager()

    store = models.ForeignKey(
        "store.Store",
        on_delete=models.SET_NULL,
        related_name="staffs",
        null=True,
    )
