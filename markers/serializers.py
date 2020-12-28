from rest_framework import serializers
from .models import Bookmark, Tag
from django.contrib.auth import get_user_model


User = get_user_model()


class BookmarksSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Bookmark
        exclude = ("id",)


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("name",)


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
