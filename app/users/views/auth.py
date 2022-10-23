from rest_framework.views import APIView


class RegisterAPIView(APIView):
    def post(self, request, *args, **kwargs):
        pass


class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        """
        TODO: check is_active before assigning token to user.
        """
        pass


class IdentityAPIView(APIView):
    def get(self, request, *args, **kwargs):
        pass


class RefreshTokenAPIView(APIView):
    def post(self, request, *args, **kwargs):
        pass


class LogoutAPIView(APIView):
    def get(self, request, *args, **kwargs):
        pass


class PasswordChangeAPIView(APIView):
    def post(self, request, *args, **kwargs):
        pass


p
