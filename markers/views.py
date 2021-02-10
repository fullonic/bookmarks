from markers.serializers import BookmarkSerializer, TagDetailSerializer, TagSerializer
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework import serializers, status, permissions
from .models import Bookmark, Tag
from rest_framework.response import Response

from markers.core import generate_tags
from django.db.models import Q


class BookmarksApiView(ListCreateAPIView):
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        # Default get bookmarks
        if not self.kwargs.get("key", False):
            return Bookmark.objects.all().order_by("-last_time_visited")[:50]

        key = self.kwargs["key"]
        # multiple searched words search will contain spaces
        keys = key.split(" ")
        return [
            Bookmark.objects.filter(Q(title__icontains=k) | Q(url__icontains=k)).all()
            for k in keys
        ]

    def list(self, request, *args, **kwargs):
        query = self.filter_queryset(self.get_queryset())
        # We need to check if it's a list to deal with multiple query parameters
        if isinstance(query, list):
            results = []
            for q in query:
                if len(q) == 0:  # ignore empty queryset
                    continue
                serializer = self.get_serializer(q, many=True)
                results += serializer.data
            return Response(data=results, status=status.HTTP_200_OK)
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        # TODO: Analyze if there is a better any of add multiple data and validate
        # allows create multiple entries
        serializer = self.get_serializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
        return super().create(request, *args, **kwargs)


class BookmarksApiViewUpdate(UpdateAPIView):
    serializer_class = BookmarkSerializer
    queryset = Bookmark.objects.all()


class TagsApiView(ListCreateAPIView):

    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly | permissions.IsAdminUser
    ]

    def create(self, request, *args, **kwargs):
        return Response(data=request.data, status=status.HTTP_201_CREATED)


class TagsApiDetail(RetrieveAPIView):
    serializer_class = TagDetailSerializer
    queryset = Tag.objects.all()
