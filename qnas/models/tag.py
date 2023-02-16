from django.db import models
from common.models import TimeModel, ViewsModel, VotesModel, CommentModel
from users.models import User



class Tag(TimeModel):
    creator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="create_tags",
        null=True,
    )
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=150)

    def __str__(self) -> str:
        return self.name