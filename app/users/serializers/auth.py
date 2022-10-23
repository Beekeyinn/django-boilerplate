from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from users.models import User


class PasswordChangeSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(
        _("Old Password"), write_only=True, required=True
    )
    new_password = serializers.CharField(
        _("New Password"), write_only=True, required=True
    )
    confirm_password = serializers.CharField(
        _("confirm Password"), write_only=True, required=True
    )

    def __init__(self, instance=None, data=..., **kwargs):
        self.request = kwargs.get("context").get("request")
        super().__init__(instance, data, **kwargs)

    class Meta:
        model = User
        fields = "__all__"

    def validate_old_password(self, value):
        user = self.request.user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "incorrect password"})
        return value

    def validate_new_password(self, value):
        """
        TODO: Add Password validation here
        """

        return value

    def validate(self, attrs):
        if (
            attrs["new_password"]
            and attrs["confirm_password"]
            and attrs["new_password"] != attrs["confirm_password"]
        ):
            raise serializers.ValidationError(
                {"confirm_password": "Passwords does not match"}
            )
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get("confirm_password"))
        instance.save()
        return instance

    def create(self, validated_data):
        raise Exception(
            f"This serializer {self.__class__} does not perform create operation"
        )


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(_("Password"), write_only=True, required=True)
    confirm_password = serializers.CharField(
        _("Confirm Password"), write_only=True, required=True
    )

    class Meta:
        model = User
        fields = ("email", "mobile", "password", "confirm_password")

    def validate_password(self, value):

        """
        TODO: Password validation here
        """
        return value

    def validate(self, attrs):
        if (
            attrs["password"]
            and attrs["confirm_password"]
            and attrs["password"] != attrs["confirm_password"]
        ):
            raise serializers.ValidationError(
                {"confirm_password": "Passwords does not match"}
            )
        return attrs

    def create(self, validated_data):
        user = User(mobile=validated_data["mobile"], email=validated_data["email"])
        user.save(commit=False)
        user.set_password(validated_data["confirm_password"])
        user.save()
        return user
