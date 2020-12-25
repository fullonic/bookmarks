from typing import Dict

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):  # type: ignore
    @classmethod
    def get_token(cls, user: User) -> Dict[str, str]:
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        # Add custom claims
        token["user"] = UserSerializer(user, many=False).data
        return token


class TokenObtainPairView(TokenObtainPairView):  # type: ignore
    serializer_class = MyTokenObtainPairSerializer
