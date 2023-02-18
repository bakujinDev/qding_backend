from django.db import models
from .user import User
from common.models import TimeModel


class Alarm(TimeModel):
    """Alarm Definition"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="alarms",
    )
    content = models.CharField(
        max_length=50,
    )
    push_url = models.URLField()
