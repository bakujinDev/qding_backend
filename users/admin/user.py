from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models.user import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        "name",
        "username",
        "last_login",
        "date_joined",
    )

    list_display_links = ("name",)

    date_hierarchy = "date_joined"

    fieldsets = (
        (
            "Profile",
            {
                "fields": (
                    "avatar",
                    "username",
                    "name",
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
