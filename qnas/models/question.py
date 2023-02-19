from django.db import models
from common.models import TimeModel, ViewsModel, VotesModel, CommentsModel
from users.models.user import User


class Question(TimeModel, ViewsModel):
    creator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="create_questions",
        null=True,
    )
    editor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="edit_questions",
        null=True,
        blank=True,
    )
    title = models.CharField(
        max_length=50,
    )
    content = models.TextField(max_length=3000)
    select_answer = models.OneToOneField(
        "qnas.Answer",
        on_delete=models.SET_NULL,
        related_name="select_question",
        default="",
        null=True,
        blank=True,
    )
    tag = models.ManyToManyField("qnas.Tag")

    def __str__(self) -> str:
        return self.title

    def answers_count(self):
        return self.answers.count()

    def votes(self):
        return self.question_votes.count()


class QuestionComment(CommentsModel):
    creator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="question_comments",
        null=True,
    )
    target = models.ForeignKey(
        Question,
        on_delete=models.SET_NULL,
        null=True,
        related_name="question_comments",
    )

    def __str__(self) -> str:
        return f"{self.creator} at {self.target}"


class QuestionVote(VotesModel):
    creator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="question_votes",
        null=True,
    )
    target = models.ForeignKey(
        Question,
        on_delete=models.SET_NULL,
        null=True,
        related_name="question_votes",
    )

    def __str__(self) -> str:
        return f"{self.votes} to {self.target}"
