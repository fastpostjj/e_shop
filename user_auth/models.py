from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _
from config.settings import NULLABLE


class User(AbstractUser):
    """
    email
    phone
    """

    username = None
    email = models.EmailField(
        unique=True,
        verbose_name=_('email')
        )
    phone = models.CharField(
        max_length=35,
        verbose_name=_('phone'),
        **NULLABLE
        )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"
