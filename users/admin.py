from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, InitUserName


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        "name",
        "username",
        "email_authentication",
        "last_login",
        "date_joined",
    )

    list_display_links = (
        "name",
        "username",
    )

    date_hierarchy = "date_joined"

    fieldsets = (
        (
            "Profile",
            {
                "fields": (
                    "avatar",
                    "username",
                    "password",
                    "name",
                    "email_authentication",
                ),
                "classes": ("wide",),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Important dates",
            {
                "fields": ("last_login", "date_joined"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(InitUserName)
class InitUserNameAdmin(admin.ModelAdmin):
    list_display = (
        "kind",
        "value",
    )
