from django.db import models
from common.models import TimeModel, ViewsModel, VotesModel, CommentsModel
from qnas import models as QnasModels
from users import models as UsersModels


class Answer(TimeModel, ViewsModel):
    creator = models.ForeignKey(
        UsersModels.User,
        on_delete=models.SET_NULL,
        related_name="answers",
        null=True,
    )
    question = models.ForeignKey(
        QnasModels.Question,
        on_delete=models.SET_NULL,
        null=True,
        related_name="answers",
    )
    content = models.TextField(max_length=3000)

    def __str__(self) -> str:
        return f"{self.creator} answered {self.question}"

    def votes(self):
        plus = self.answer_votes.filter(vote_type="plus").count()
        minus = self.answer_votes.filter(vote_type="minus").count()

        return plus - minus

    def is_selected(self):
        return self == self.question.select_answer


class AnswerComment(CommentsModel):
    creator = models.ForeignKey(
        UsersModels.User,
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


class AnswerVote(VotesModel):
    creator = models.ForeignKey(
        UsersModels.User,
        on_delete=models.SET_NULL,
        related_name="answer_votes",
        null=True,
    )
    target = models.ForeignKey(
        Answer,
        on_delete=models.SET_NULL,
        null=True,
        related_name="answer_votes",
    )

    def __str__(self) -> str:
        return f"{self.vote_type} to {self.target}"
