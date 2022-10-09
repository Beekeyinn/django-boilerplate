from app.users.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# Register your models here.
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ["email", "mobile", "is_active", "is_admin", "is_superuser"]
    list_filter = ["is_admin", "is_active", "is_superuser"]

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
    )

    add_fieldsets = (
        None,
        {
            "classes": ("wide",),
            "fields": ("email", "mobile", "password1", "password2"),
        },
    )

    search_fields = (
        "email",
        "mobile",
    )
    ordering = ("email",)
    filter_horizontal = ()
