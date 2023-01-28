from django.db import models
from common.models import TimeModel, ViewsModel, VotesModel
from users.models import User
from questions.models import Question


class Answer(TimeModel, ViewsModel, VotesModel):
    question = models.ForeignKey(
        Question,
        on_delete=models.SET_NULL,
        null=True,
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="answers",
        null=True,
    )
    content = models.TextField(max_length=3000)

    def __str__(self) -> str:
        return f"{self.creator} answered ${self.question}"
