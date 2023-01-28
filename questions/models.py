from django.db import models
from common.models import TimeModel, ViewsModel, VotesModel
from users.models import User


class Question(TimeModel, ViewsModel, VotesModel):
    creator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="creator",
        null=True,
    )
    editor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="editor",
        null=True,
        blank=True,
    )
    title = models.CharField(
        max_length=50,
    )
    content = models.TextField(max_length=3000)
    # tag= models.ManyToManyField(to)
