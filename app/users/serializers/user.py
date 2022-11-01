from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        exclude = [
            "is_superuser",
            "groups",
            "user_permissions",
            "is_admin",
            "last_login",
            "password",
        ]
        read_only_fields = [
            "email",
            "is_active",
            "created_at",
            "updated_at",
        ]

    # def __init__(self, instance=None, data=..., **kwargs) -> None:
    #     if kwargs.get("context", None) is not None:
    #         self.request = kwargs["context"].get("request", None)
    #     super().__init__(instance, data, **kwargs)

    # def get_extra_kwargs(self) -> Union[Any, Dict]:
    #     extra_kwargs = super().get_extra_kwargs()
    #     request = self.request
    #     if request is not None:
    #         if request.method == "PUT" or request.method == "PATCH":
    #             extra_kwargs["mobile"]["read_only"] = True
    #         elif request.method == "POST":
    #             extra_kwargs["password"]["read_only"] = False
    #     return extra_kwargs
