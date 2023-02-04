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
    content = models.TextField()
    select_answer = models.OneToOneField(
        "qnas.Answer",
        on_delete=models.SET_NULL,
        related_name="select_question",
        default="",
        null=True,
        blank=True,
    )
    view_count = models.PositiveIntegerField(default=0, help_text="조회수 / 쿠키 기반 중복 방지")
    # tag= models.ManyToManyField(to)

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
