from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.forms import UserChangeForm, UserCreationForm
from users.models.user import User


# Register your models here.
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = [
        "email",
        "mobile",
        "is_active",
        "is_admin",
        "is_superuser",
    ]
    list_filter = [
        "is_admin",
        "is_active",
        "is_superuser",
    ]
    readonly_fields = [
        "mobile",
        "created_at",
        "updated_at",
    ]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        ("Personal Information", {"fields": ("mobile",)}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_admin",
                    "is_superuser",
                )
            },
        ),
        (
            "Extra",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "mobile", "password1", "password2"),
            },
        ),
    )

    search_fields = (
        "email",
        "mobile",
    )
    ordering = ("email",)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
