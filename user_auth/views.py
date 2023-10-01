from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets, status
from rest_framework.response import Response
from user_auth.models import User
from django.contrib.auth.hashers import make_password
from user_auth.serializer import UsersSerializers, GetTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UsersSerializers
    queryset = User.objects.all().order_by('date_joined')


class GetTokenObtainPairView(TokenObtainPairView):
    """
     представление для получения JWT-токена.
    """
    serializer_class = GetTokenObtainPairSerializer
