from core.permissions import IsOwnerOrIsAdmin
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models.user import User
from users.serializers.user import UserSerializer


class UserListAPIView(APIView):
    permission_classes = [IsAuthenticated | IsAdminUser & IsOwnerOrIsAdmin]

    def get(self, request, *args, **kwargs) -> Response:
        users = User.objects.all()
        serializer = UserSerializer(users, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
