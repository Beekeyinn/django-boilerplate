from typing import Any, Dict, Union

from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            "email",
            "mobile",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "is_active",
            "created_at",
            "updated_at",
        ]

    def __init__(self, instance=None, data=..., **kwargs) -> None:
        self.request = kwargs["context"].get("request", None)
        super().__init__(instance, data, **kwargs)

    def get_extra_kwargs(self) -> Union[Any, Dict]:
        extra_kwargs = super().get_extra_kwargs()
        request = self.request
        if request is not None:
            if request.method == "PUT" or request.method == "PATCH":
                extra_kwargs["mobile"]["read_only"] = True
            elif request.method == "POST":
                extra_kwargs["password"]["read_only"] = False
        return extra_kwargs
