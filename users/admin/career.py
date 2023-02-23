from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users import models


@admin.register(models.Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "position",
        "company",
    )
