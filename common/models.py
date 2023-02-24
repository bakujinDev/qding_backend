from django.db import models


class TimeModel(models.Model):
    """Time Model Definition"""

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        abstract = True


class ViewsModel(models.Model):
    """Views Model Definition"""

    views = models.PositiveIntegerField(
        default=0,
        editable=False,
        help_text="조회수 / 쿠키 기반 중복 방지",
    )

    class Meta:
        abstract = True


class VotesModel(TimeModel):
    """Votes Model Definition"""

    class VoteKindChoices(models.TextChoices):
        Plus = "plus", "Plus"
        Minus = "minus", "Minus"

    vote_type = models.CharField(
        max_length=6,
        choices=VoteKindChoices.choices,
    )
    target_updated = models.DateTimeField(null=True)

    class Meta:
        abstract = True


class CommentsModel(TimeModel):
    content = models.TextField(max_length=200)

    class Meta:
        abstract = True
