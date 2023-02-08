from django.contrib import admin
from .models import Photo


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = (
        "creator",
        "category",
        "file",
        "updated_at",
    )

    list_display_links = ("file",)

    date_hierarchy = "updated_at"
