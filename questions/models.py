from django.db import models
from common.models import CommonModel
from users.models import User


class Question(CommonModel):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="reviews",
        null=True,
    )
    # tag= models.ManyToManyField(to)
