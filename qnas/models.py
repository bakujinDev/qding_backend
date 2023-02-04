from django.db import models
from common.models import TimeModel, ViewsModel, VotesModel
from users.models import User


class Question(TimeModel, ViewsModel, VotesModel):
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

    def answers_count(self):
        return self.answers.count()

    def __str__(self) -> str:
        return self.title


class Answer(TimeModel, ViewsModel, VotesModel):
    question = models.ForeignKey(
        Question, on_delete=models.SET_NULL, null=True, related_name="answers"
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="answers",
        null=True,
    )
    content = models.TextField(max_length=3000)

    def __str__(self) -> str:
        return f"{self.creator} answered {self.question}"


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
