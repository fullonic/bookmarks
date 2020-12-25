from rest_framework import serializers
from .models import Bookmark


class BookmarksSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        many = kwargs.pop("many", True)
        super().__init__(many=many, *args, **kwargs)

    class Meta:
        model = Bookmark
        exclude = ("tags", "id")
