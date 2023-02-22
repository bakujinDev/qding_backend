from django.contrib import admin
from . import models


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "creator",
        "title",
        "votes",
        "views",
        "updated_at",
    )

    list_filter = ("tag",)
    list_display_links = ("title",)

    date_hierarchy = "updated_at"


@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        "creator",
        "question",
        "content",
        "votes",
        "is_selected",
        "updated_at",
    )

    list_filter = ("question__tag",)
    list_display_links = ("content",)

    date_hierarchy = "updated_at"


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "creator",
        "created_at",
    )


@admin.register(models.QuestionComment, models.AnswerComment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "creator",
        "target",
        "updated_at",
        "content",
    )

    list_display_links = ("content",)

    date_hierarchy = "updated_at"


@admin.register(models.QuestionVote)
class VotesAdmin(admin.ModelAdmin):
    list_display = (
        "creator",
        "target",
        "created_at",
    )
