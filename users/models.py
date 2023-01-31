from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField(
        max_length=150,
        editable=False,
    )
    last_name = models.CharField(
        max_length=150,
        editable=False,
    )
    name = models.CharField(
        max_length=30,
    )
    avatar = models.URLField(
        blank=True,
    )


class InitUserName(models.Model):
    """Init UserName Definition"""

    class NameKindChoices(models.TextChoices):
        HEADER = "header", "Header"
        FOOTER = "footer", "Footer"

    kind = models.CharField(
        max_length=15,
        choices=NameKindChoices.choices,
    )
    value = models.CharField(max_length=8)

    def __str__(self):
        return f"{self.kind} / ${self.value}"
