from markers.serializers import BookmarksSerializer
from rest_framework.generics import ListCreateAPIView
from rest_framework import status
from .models import Bookmark
from rest_framework.response import Response


class BookmarksApiView(ListCreateAPIView):
    serializer_class = BookmarksSerializer
    queryset = Bookmark.objects.all()

    def create(self, request, *args, **kwargs):
        return Response(data=request.data, status=status.HTTP_201_CREATED)
