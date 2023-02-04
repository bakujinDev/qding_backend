from django.contrib import admin
from .models import Question, Answer


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "creator",
        "title",
        "votes",
        "view_count",
        "updated_at",
    )

    list_display_links = ("title",)

    date_hierarchy = "updated_at"


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        "creator",
        "question",
        "votes",
        "updated_at",
    )

    date_hierarchy = "updated_at"
