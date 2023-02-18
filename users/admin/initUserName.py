from django.contrib import admin
from users.models.initUserName import InitUserName


@admin.register(InitUserName)
class InitUserNameAdmin(admin.ModelAdmin):
    list_display = (
        "kind",
        "value",
    )
