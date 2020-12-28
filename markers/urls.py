from django.urls import path
from .views import BookmarksApiView, TagsApiView

from .custom_claims import TokenObtainPairView

urlpatterns = [
    path("bookmarks", BookmarksApiView.as_view(), name="bookmarks-list"),
    path("tags", TagsApiView.as_view(), name="tags-list"),
    path("login/", TokenObtainPairView.as_view()),
]
