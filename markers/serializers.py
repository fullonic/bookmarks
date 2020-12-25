from rest_framework import serializers
from .models import Bookmark
from django.contrib.auth import get_user_model


User = get_user_model()


class BookmarksSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        many = kwargs.pop("many", True)
        super().__init__(many=many, *args, **kwargs)

    class Meta:
        model = Bookmark
        exclude = ("tags", "id")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "password",
            "user_permissions",
            "groups",
            "is_staff",
            "is_active",
            "is_superuser",
            "last_login",
        )
