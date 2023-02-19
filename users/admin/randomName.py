from django.contrib import admin
from users.models.randomName import RandomName


@admin.register(RandomName)
class RandomNameAdmin(admin.ModelAdmin):
    list_display = (
        "kind",
        "value",
    )
