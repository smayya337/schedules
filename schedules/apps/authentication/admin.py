from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    search_fields = ["username", "preferred_name", "last_name"]
    list_display = ["username", "last_name", "preferred_name", "last_modified"]
    list_filter = ["accepted_terms", "publish_data"]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "first_name",
                    "last_name",
                    "nickname",
                    "email",
                    "password",
                    "accepted_terms",
                    "is_staff",
                    "is_superuser",
                    "graduation_year",
                    "is_student",
                    "last_modified",
                    "last_login",
                )
            },
        ),
    )

    readonly_fields = (
        "last_modified",
        "last_login",
    )


admin.site.register(User, UserAdmin)
