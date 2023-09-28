from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from django.db import models
from rest_framework import serializers
from user_auth.models import User


class UsersSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'email',
            'phone'
        )


class GetTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Сериализатор  GetTokenObtainPairSerializer  для обработки запросов на получение токена"""
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Добавление пользовательских полей в токен
        token['username'] = user.username
        token['email'] = user.email
        return token
