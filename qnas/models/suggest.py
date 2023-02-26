from django.db import models
from common.models import TimeModel
from users.models import *


class QuestionEdit(TimeModel):
    suggester = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="question_edit",
        null=True,
    )
    target = models.ForeignKey(
        Question,
        on_delete=models.SET_NULL,
        null=True,
        related_name="question_edit",
    )
    title = models.CharField(
        max_length=50,
    )
    content = models.TextField(max_length=3000)
    tag = models.ManyToManyField(
        "qnas.Tag",
        related_name="question_edit",
    )
