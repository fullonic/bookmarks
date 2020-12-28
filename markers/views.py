from markers.serializers import BookmarksSerializer, TagsSerializer
from rest_framework.generics import ListCreateAPIView
from rest_framework import status, permissions
from .models import Bookmark, Tag
from rest_framework.response import Response

from markers.core import generate_tags


class BookmarksApiView(ListCreateAPIView):
    serializer_class = BookmarksSerializer
    queryset = Bookmark.objects.all()
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly | permissions.IsAdminUser
    ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=request.data, status=status.HTTP_201_CREATED)
        return super().create(request, *args, **kwargs)


class TagsApiView(ListCreateAPIView):

    serializer_class = TagsSerializer
    queryset = Tag.objects.all()
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly | permissions.IsAdminUser
    ]

    def create(self, request, *args, **kwargs):
        return Response(data=request.data, status=status.HTTP_201_CREATED)
