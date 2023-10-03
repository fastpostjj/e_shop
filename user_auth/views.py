from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets
from user_auth.models import User
from user_auth.serializer import UsersSerializers, GetTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    Представление для модели User
    """
    serializer_class = UsersSerializers
    queryset = User.objects.all().order_by('date_joined')


class GetTokenObtainPairView(TokenObtainPairView):
    """
    Представление для получения JWT-токена.
    """
    serializer_class = GetTokenObtainPairSerializer
