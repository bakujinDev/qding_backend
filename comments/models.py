from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from common.models import TimeModel
from users.models import User


class Comment(TimeModel):
    target_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField()
    target = GenericForeignKey("target_type", "target_id")
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        null=True,
    )
    content = models.TextField(max_length=200)

    def __str__(self):
        return f"{self.creator} commented {self.target}"

    class Meta:
        indexes = [
            models.Index(fields=["target_type", "target_id"]),
        ]
