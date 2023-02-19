from django.contrib import admin
from users.models import *


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "content",
        "push_url",
        "updated_at",
    )

    date_hierarchy = "updated_at"
