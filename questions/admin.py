from django.contrib import admin
from .models import Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "creator",
        "title",
        "votes",
        "updated_at",
    )
