from core.auth import user_authentication
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from users.models import User
from users.serializers import UserSerializer


class PasswordChangeSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(
        label=_("Old Password"), write_only=True, required=True
    )
    new_password = serializers.CharField(
        label=_("New Password"), write_only=True, required=True
    )
    confirm_password = serializers.CharField(
        label=_("confirm Password"), write_only=True, required=True
    )

    def __init__(self, *args, **kwargs) -> None:
        self.request = kwargs.get("context").get("request")
        super().__init__()

    class Meta:
        model = User
        fields = "__all__"

    def validate_old_password(self, value) -> str:
        user = self.request.user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "incorrect password"})
        return value

    def validate_new_password(self, value) -> str:
        """
        TODO: Add Password validation here
        """

        return value

    def validate(self, attrs) -> dict:
        if (
            attrs["new_password"]
            and attrs["confirm_password"]
            and attrs["new_password"] != attrs["confirm_password"]
        ):
            raise serializers.ValidationError(
                {"confirm_password": "Passwords does not match"}
            )
        return attrs

    def update(self, instance, validated_data) -> User:
        instance.set_password(validated_data.get("confirm_password"))
        instance.save()
        return instance

    def create(self, validated_data) -> None:
        raise Exception(
            f"This serializer {self.__class__} does not perform create operation"
        )


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        label=_("Password"), write_only=True, required=True
    )
    confirm_password = serializers.CharField(
        label=_("Confirm Password"), write_only=True, required=True
    )

    class Meta:
        model = User
        fields = ("email", "mobile", "password", "confirm_password")

    def validate_password(self, value) -> str:

        """
        TODO: Password validation here
        """
        return value

    def validate(self, attrs) -> dict:
        if (
            attrs["password"]
            and attrs["confirm_password"]
            and attrs["password"] != attrs["confirm_password"]
        ):
            raise serializers.ValidationError(
                {"confirm_password": "Passwords does not match"}
            )
        return attrs

    def create(self, validated_data) -> User:
        user = User(mobile=validated_data["mobile"], email=validated_data["email"])
        user.set_password(validated_data["confirm_password"])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """
    username can be both mobile and email address
    """

    username = serializers.CharField(
        label=_("Username"), required=True, write_only=True
    )
    password = serializers.CharField(
        label=_("Password"), required=True, write_only=True
    )

    def validate_username(self, value: str) -> str:
        """
        TODO: Validate whether the value is digit or not and if it is delete check if there exist any user for that mobile number
        TODO: check if the value is an email address, check if user with that email address exists or not then add user if exists

        if isinstance(username, int):
            _username = User.objects.get(mobile=username).email
        else:
            _username = username

        """
        if value.isdigit():
            if User.objects.filter(mobile=value).exists():
                email = User.objects.get(mobile=value).email
                return email

            raise serializers.ValidationError({"username": "User does not exist."})
        else:
            return value

    def authenticate(self) -> dict:
        user, token = user_authentication(
            self.validated_data.get("username"), self.validated_data.get("password")
        )
        serializer = UserSerializer(user)
        return {
            "detail": serializer.data,
            "access_token": token.get("access_token"),
            "refresh_token": token.get("refresh_token"),
        }
