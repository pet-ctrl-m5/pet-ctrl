from django.contrib.auth.models import BaseUserManager
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def _create_user(
        self, username, password, is_superuser, is_manager, is_doctor, **extra_fields
    ):
        now = timezone.now()

        user = self.model(
            username=username,
            is_superuser=is_superuser,
            is_manager=is_manager,
            is_doctor=is_doctor,
            is_active=True,
            **extra_fields
        )
        user.set_password(password)

        user.save(using=self.db)

        return user

    def create_superuser(self, username, password, **extra_fields):
        return self._create_user(username, password, True, True, False, **extra_fields)

    def create_user(self, username, password, is_manager, is_doctor, **extra_fields):
        return self._create_user(
            username, password, False, is_manager, is_doctor, **extra_fields
        )
