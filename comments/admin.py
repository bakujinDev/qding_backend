from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = (
        "target",
        "creator",
        "updated_at",
    )
    
    date_hierarchy = "updated_at"
