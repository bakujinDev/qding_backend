from django.contrib import admin
from .models import Question, QuestionComment, Answer, AnswerComment, Tag


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "creator",
        "title",
        "votes",
        "views",
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


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "creator",
        "created_at",
    )


@admin.register(QuestionComment, AnswerComment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "creator",
        "target",
        "updated_at",
        "content",
    )

    list_display_links = ("content",)

    date_hierarchy = "updated_at"
