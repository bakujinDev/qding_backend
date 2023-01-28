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
    )

    class Meta:
        abstract = True


class VotesModel(models.Model):
    """Votes Model Definition"""

    votes = models.IntegerField(
        default=0,
        editable=False,
    )

    class Meta:
        abstract = True
