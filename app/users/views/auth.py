from core.auth import UserCacheManagement
from core.decorator import exception_grabber
from django.core.cache import cache
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import LoginSerializer, RegisterSerializer
from users.serializers.user import UserSerializer


class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer

    @exception_grabber
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(data={"success": True}, status=status.HTTP_201_CREATED)


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    @exception_grabber
    def post(self, request, *args, **kwargs):
        serializer: LoginSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.authenticate()
        return Response(data, status=status.HTTP_200_OK)


class IdentityAPIView(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@exception_grabber
@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        title="Refresh Token View",
        description="Generate new access token using the before refresh token if not expired",
        type=openapi.TYPE_OBJECT,
        properties={
            "refresh": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Refresh Token -> for gaining new access token",
                required="true",
            ),
        },
    ),
    responses={
        200: """{
                "access_token": openapi.TYPE_STRING,
                "refresh_token": openapi.TYPE_STRING,
            }"""
    },
)
@api_view(["post"])
def refresh_token_api_view(request, *args, **kwargs):

    data = request.data

    token = cache.get(data.get("refresh"))
    if token:
        tokens = UserCacheManagement.get_refreshed_token(data)
        return Response(tokens, status=status.HTTP_200_OK)
    return Response(
        data={"error": "invalid token. please login"},
        status=status.HTTP_400_BAD_REQUEST,
    )


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        refresh_token = cache.get(request.auth)
        cache.delete(cache.get(refresh_token))
        cache.delete(refresh_token)
        cache.delete(f"user_{refresh_token}")


class PasswordChangeAPIView(APIView):
    def post(self, request, *args, **kwargs):
        pass
