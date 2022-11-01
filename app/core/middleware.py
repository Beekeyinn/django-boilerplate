import re
from typing import Any
from urllib import response

from django.conf import settings
from django.http import HttpRequest
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from core.auth import UserCacheManagement


def require_authentication(request: HttpRequest):
    for url in settings.LOGIN_NOT_REQUIRED_URLS:
        if re.compile(url).match(request.path):
            return False
    return True


def middleware_response_generator(response: Any):
    response.accepted_renderer = JSONRenderer()
    response.accepted_media_type = "application/json"
    response.renderer_context = {}
    response.render()
    return response


class AuthorizationMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest, *args: Any, **kwds: Any) -> Any:
        if require_authentication(request):
            setattr(request, "require_authentication", True)
            response = self.get_response(request)
            return response
        else:
            response = self.get_response(request)
            return response


class APIAuthenticationMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest, *args, **kwargs) -> response:
        if hasattr(request, "require_authentication"):
            delattr(request, "require_authentication")
            authorization_key: str = request.META.get(
                settings.SIMPLE_JWT.get("AUTH_HEADER_NAME")
            )
            if not authorization_key:
                response = Response(
                    {"detail": "Authentication credential were not provided."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
                return middleware_response_generator(response)
            key_type, key = authorization_key.split()
            if not key_type in settings.SIMPLE_JWT.get("AUTH_HEADER_TYPES"):
                response = Response(
                    {"detail": "Invalid Token Type"},
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )
                return middleware_response_generator(response)
            request.user = UserCacheManagement.get_user(token=key)
            response = self.get_response(request)
            return response
        else:   
            response = self.get_response(request)
            return response
