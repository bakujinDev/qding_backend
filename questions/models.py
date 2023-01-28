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
        "answers.Answer",
        on_delete=models.SET_NULL,
        related_name="select_question",
        default='',
        null=True,
        blank=True,
    )
    # tag= models.ManyToManyField(to)

    def __str__(self) -> str:
        return self.title
