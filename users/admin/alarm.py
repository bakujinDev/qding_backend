from django.contrib import admin
from users.models.alarm import Alarm


@admin.register(Alarm)
class AlarmAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "content",
        "push_url",
        "updated_at",
    )

    date_hierarchy = "updated_at"
