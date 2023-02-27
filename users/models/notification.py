from django.db import models
from .user import User
from common.models import TimeModel


class Notification(TimeModel):
    """Notification Definition"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    content = models.CharField(
        max_length=50,
    )
    push_url = models.URLField()

    def __str__(self):
        return f"{self.user} / {self.content}"
