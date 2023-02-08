from django.db import models
from common.models import TimeModel
from users.models import User


class Photo(TimeModel):
    class CategoryKindChoices(models.TextChoices):
        Qna_Question = "qna_question", "Qna_Question"
        Qna_Answer = "qna_answer", "Qna_Answer"
        Profile_Img = "profile_image", "Profile_Image"

    creator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="create_photos",
        null=True,
    )
    file = models.URLField()
    category = models.CharField(
        max_length=15,
        choices=CategoryKindChoices.choices,
        default='qna_answer',
        null=True,
    )
