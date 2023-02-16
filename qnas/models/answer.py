from django.db import models
from .question import Question
from common.models import TimeModel, ViewsModel, VotesModel, CommentModel
from users.models import User


class Answer(TimeModel, ViewsModel, VotesModel):
    creator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="answers",
        null=True,
    )
    question = models.ForeignKey(
        Question, on_delete=models.SET_NULL, null=True, related_name="answers"
    )
    content = models.TextField(max_length=3000)

    def __str__(self) -> str:
        return f"{self.creator} answered {self.question}"


class AnswerComment(CommentModel):
    creator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="answer_comments",
        null=True,
    )
    target = models.ForeignKey(
        Answer,
        on_delete=models.SET_NULL,
        null=True,
        related_name="answer_comments",
    )

    def __str__(self) -> str:
        return f"{self.creator} at {self.target}"
