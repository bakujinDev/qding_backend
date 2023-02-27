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
        editable=False,
    )

    name = models.CharField(
        max_length=30,
        unique=True,
    )
    avatar = models.URLField(
        blank=True,
    )
    introduce = models.CharField(
        max_length=120,
        default="",
        null=True,
        blank=True,
    )
    blog = models.URLField(
        null=True,
        blank=True,
    )
    github = models.URLField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name
