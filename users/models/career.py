from django.db import models
from django.contrib.auth.models import AbstractUser
from .user import User
from common.models import TimeModel

class Career(TimeModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="careers",
    )
    company = models.CharField(max_length=30)
    position = models.CharField(max_length=30)
    first_day = models.DateField()
    last_day = models.DateField()

    def __str__(self):
        return f"{self.user} / {self.position} / {self.company}"
