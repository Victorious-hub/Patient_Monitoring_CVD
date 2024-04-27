from rest_framework import views, status
from rest_framework.response import Response
from .services import AuthService
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class UserLogoutAPi(views.APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            print(refresh_token)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class TokenObtainPairAPIView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class ObtainTokenAPIView(views.APIView):
    def post(self, request):
        serializer = TokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token_data = serializer.validated_data

        user_role = AuthService(request.data['email'])
        token_data['role'] = user_role.role_get()
        return Response(token_data, status=status.HTTP_201_CREATED)
