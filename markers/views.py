from markers.serializers import BookmarkSerializer, TagDetailSerializer, TagSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework import status, permissions
from .models import Bookmark, Tag
from rest_framework.response import Response

from markers.core import generate_tags


class BookmarksApiView(ListCreateAPIView):
    serializer_class = BookmarkSerializer
    queryset = Bookmark.objects.all()
    # permission_classes = [
    #     permissions.IsAuthenticatedOrReadOnly | permissions.IsAdminUser
    # ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=request.data, status=status.HTTP_201_CREATED)
        return super().create(request, *args, **kwargs)


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
