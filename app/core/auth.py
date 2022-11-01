from typing import Dict, Optional, Union

import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User

REFRESH_TOKEN_LIFETIME: float = settings.SIMPLE_JWT.get(
    "REFRESH_TOKEN_LIFETIME"
).total_seconds()
ACCESS_TOKEN_LIFETIME: float = settings.SIMPLE_JWT.get(
    "ACCESS_TOKEN_LIFETIME"
).total_seconds()


class UserCacheManagement:

    """
    cache -> (access token, refresh token)
    cache -> (refresh token, access token)
    cache -> (user_{refresh_token}, user)
    """

    _access_token_lifetime: float = ACCESS_TOKEN_LIFETIME
    _refresh_token_lifetime: float = REFRESH_TOKEN_LIFETIME

    def __init__(
        self, token: Union[RefreshToken, str], refresh_token: Optional[str] = None
    ) -> None:
        if isinstance(token, RefreshToken):
            self.token: str = str(token.access_token)
            self.refresh_token: str = str(token)
        else:
            self.token = token
            self.refresh_token = refresh_token

    def get_user_id(self) -> int:

        token_payload = jwt.decode(
            self.token,
            key=settings.SIMPLE_JWT.get("SIGNING_KEY"),
            algorithms=[
                settings.SIMPLE_JWT.get("ALGORITHM"),
            ],
        )

        user_id = token_payload.get("user_id")
        return int(user_id)

    @property
    def user(self) -> User:
        user_id = self.get_user_id()
        try:
            user = User.objects.get(id=user_id)
            return user
        except User.DoesNotExist as e:
            raise ObjectDoesNotExist(e)

    @classmethod
    def get_user(cls, token) -> User:
        user = cache.get(f"user_{cache.get(token)}")
        if user:
            return user
        raise Exception("error occurred")

    def get_tokens(self) -> dict:
        if self.refresh_token and self.token:
            return {"access_token": self.token, "refresh_token": self.refresh_token}
        return {"refresh_token": self.refresh_token}

    def set_caches(self) -> bool:
        if self.refresh_token and self.token:
            cache.set(self.refresh_token, self.token, self._refresh_token_lifetime)
            cache.set(self.token, self.refresh_token, self._access_token_lifetime)
            cache.set(
                f"user_{self.refresh_token}", self.user, self._refresh_token_lifetime
            )
            return True
        return False

    @classmethod
    def get_refreshed_token(cls, refresh: dict) -> Dict:
        _refresh = refresh.get("refresh")
        old_access_token = cache.get(_refresh)
        rs = TokenRefreshSerializer(data=refresh)
        rs.is_valid(raise_exception=True)
        new_token = cls(
            token=rs.validated_data.get("access"),
            refresh_token=rs.validated_data.get("refresh"),
        )
        new_token.set_caches()
        tokens = new_token.get_tokens()
        cache.delete(_refresh)
        cache.delete(f"user_{_refresh}")
        cache.delete(old_access_token)
  
        return tokens


def set_cache(token: RefreshToken, user: User) -> dict:
    tokens = {"access_token": str(token.access_token), "refresh_token": str(token)}
    cache.set(tokens["refresh_token"], tokens["access_token"], REFRESH_TOKEN_LIFETIME)
    cache.set(tokens["access_token"], tokens["refresh_token"], ACCESS_TOKEN_LIFETIME)
    cache.set(f"user_{tokens['refresh_token']}", user, REFRESH_TOKEN_LIFETIME)
    return tokens


def user_authentication(username: str, password: str) -> User:
    user = authenticate(email=username, password=password)

    if not user:
        raise AuthenticationFailed()
    token: RefreshToken = RefreshToken.for_user(user)

    tokens = set_cache(token, user)
    return user, tokens
