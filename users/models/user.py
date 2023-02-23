from django.db import models
from django.contrib.auth.models import AbstractUser
from common.models import TimeModel


class User(AbstractUser):
    first_name = models.CharField(
        max_length=150,
        editable=False,
    )
    last_name = models.CharField(
        max_length=150,
        editable=False,
    )
    email = models.CharField(
        max_length=150,
    )
    name = models.CharField(
        max_length=30,
        unique=True,
    )
    avatar = models.URLField(
        blank=True,
    )
    email_authentication = models.BooleanField(
        default=False, help_text="authentication by email"
    )
    message = models.CharField(
        max_length=120,
        default="",
        null=True,
    )
    blog = models.URLField(null=True)
    github = models.URLField(null=True)

    def __str__(self):
        return self.name

