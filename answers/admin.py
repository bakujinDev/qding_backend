from django.contrib import admin
from .models import Answer


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        "creator",
        "question",
        "votes",
        "updated_at",
    )
