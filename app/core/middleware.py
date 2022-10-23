from typing import Dict, Union
from urllib import response

import jwt
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest
from rest_framework.exceptions import NotAuthenticated
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from users.models import User

from core.custom_exceptions import InvalidTokenType


class UserCacheManagement:

    """
    cache -> (access token, refresh token)
    cache -> (refresh token, access token)
    cache -> (user_{refresh_token}, user)
    """

    _access_token_lifetime: float = settings.SIMPLE_JWT.get(
        "ACCESS_TOKEN_LIFETIME"
    ).total_seconds()
    _refresh_token_lifetime: float = settings.SIMPLE_JWT.get(
        "REFRESH_TOKEN_LIFETIME"
    ).total_seconds()

    def __init__(
        self, token: str, refresh_token: Union[str, None], expire_time: float
    ) -> None:
        self.token = token
        if refresh_token:
            self.refresh_token = refresh_token
        self.expire_time = expire_time

    @property
    def user(self) -> User:
        token_payload = jwt.decode(self.token)
        if token_payload.token_type == "access":
            user_id = token_payload.get("user_id")
            try:
                user = User.objects.get(id=user_id)
                return user
            except User.DoesNotExist as e:
                raise ObjectDoesNotExist(e.args[0])
        raise InvalidToken()

    @classmethod
    def get_user(cls, token):
        return cache.get(f"user__{cache.get(token)}")

    def set_caches(self) -> bool:
        """
        TODO: assign tokens in cache with expire time
        """
        cache.set(self.refresh_token, self.token, self._refresh_token_lifetime)
        cache.set(self.token, self.refresh_token, self._access_token_lifetime)
        payload = jwt.decode(self.token)
        cache.set(f"user_{self.refresh_token}", self.user, self._refresh_token_lifetime)
        return True

    @classmethod
    def get_refreshed_token(cls, refresh: str) -> Dict:
        if refresh and cache.get(refresh):
            old_access_token = cache.get(refresh)
            rs = TokenRefreshSerializer(refresh)
            try:
                rs.is_valid(raise_exception=True)
            except Exception as e:
                raise Exception(e.args[0])
            cache.delete(refresh)
            cache.delete(f"user_{refresh}")
            cache.delete(old_access_token)
            new_token = cls(
                token=rs.validated_data.get("access"),
                refresh_token=rs.validated_data.get("refresh"),
            )
            new_token.set_caches()
        else:
            raise Exception("Refresh Token Black Listed. Login Again")
        return {"access": str(new_token.token), "refresh": str(new_token.refresh_token)}


class APIAuthenticationMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response
        self.login_not_required_urls = tuple(
            [url for url in settings.LOGIN_NOT_REQUIRED_URLS]
        )

    def __call__(self, request: HttpRequest, *args, **kwargs) -> response:
        if not request.path in self.login_not_required_urls:
            authorization_key: str = request.META.get(
                settings.SIMPLE_JWT.get("AUTH_HEADER_NAME")
            )
            if authorization_key:
                key, key_type = authorization_key.split()
                if key_type not in settings.SIMPLE_JWT.get("AUTH_HEADER_TYPES"):
                    raise InvalidTokenType()
                request.user = UserCacheManagement.get_user(token=key)
                if request.user:
                    request.is_authenticated = True
                else:
                    request.is_authenticated = False
                response = self.get_response(request)
                return response
            else:
                raise NotAuthenticated()
        else:
            return self.get_response(request)
