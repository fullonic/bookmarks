from markers.serializers import BookmarkSerializer, TagDetailSerializer, TagSerializer
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework import serializers, status, permissions
from .models import Bookmark, Tag
from rest_framework.response import Response

from markers.core import generate_tags
from django.db.models import Q


class BookmarksApiView(ListCreateAPIView):
    serializer_class = BookmarkSerializer

    def get_queryset(self):
        # not a filter query, ruturns all bookmarks collection
        if not self.kwargs.get("key", False):
            return Bookmark.objects.all().order_by("-last_time_visited")

        # filter query
        key = self.kwargs["key"]
        # multiple word search will contain spaces
        if " " in key:  # single word search
            keys = key.split(" ")
            return [
                Bookmark.objects.filter(
                    Q(title__icontains=k) | Q(url__icontains=k)
                ).all()
                for k in keys
            ]
        # single word query
        return Bookmark.objects.filter(
            Q(title__icontains=key) | Q(url__icontains=key)
        ).all()

    def list(self, request, *args, **kwargs):
        query = self.filter_queryset(self.get_queryset())
        # if the query set is a list of queries
        if isinstance(query, list):
            results = []
            for q in query:
                if len(q) == 0:  # ignore empty queryset
                    continue
                serializer = self.get_serializer(q, many=True)
                results.append(serializer.data[0])
            return Response(results)
        # for a single queryset we use the default method call
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        # allows create multiple entries
        serializer = self.get_serializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=request.data, status=status.HTTP_201_CREATED)
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
