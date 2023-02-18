from django.db import models


class InitUserName(models.Model):
    """Init UserName Definition"""

    class NameKindChoices(models.TextChoices):
        HEADER = "header", "Header"
        FOOTER = "footer", "Footer"

    kind = models.CharField(
        max_length=15,
        choices=NameKindChoices.choices,
    )
    value = models.CharField(max_length=8)

    def __str__(self):
        return f"{self.kind} / ${self.value}"
