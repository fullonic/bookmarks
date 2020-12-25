from django.urls import path
from .views import BookmarksApiView


urlpatterns = [path("bookmarks", BookmarksApiView.as_view(), name="bookmarks-list")]
