from attr import fields
from rest_framework import serializers
from .models import Bookmark, Tag
from django.contrib.auth import get_user_model


User = get_user_model()


class BookmarkSerializer(serializers.HyperlinkedModelSerializer):
    tags = serializers.HyperlinkedRelatedField(
        many=True, view_name="tag-detail", read_only=True
    )

    class Meta:
        model = Bookmark
        fields = ["url", "title", "last_time_visited", "tags"]


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ("name", "url")


class TagDetailSerializer(serializers.ModelSerializer):
    bookmark_set = serializers.StringRelatedField(many=True)

    class Meta:
        model = Tag
        fields = ("name", "url", "bookmark_set")


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
