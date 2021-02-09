from django.urls import path, re_path
from .views import BookmarksApiView, TagsApiView, TagsApiDetail, BookmarksApiViewUpdate
from .custom_claims import TokenObtainPairView

urlpatterns = [
    path("bookmarks", BookmarksApiView.as_view(), name="bookmark-list"),
    path("bookmarks/<int:pk>", BookmarksApiViewUpdate.as_view(), name="bookmark-update"),
    re_path(
        "^bookmarks/(?P<key>.+)/$",
        BookmarksApiView.as_view(),
        name="bookmark-list",
    ),
    path("tags", TagsApiView.as_view(), name="tag-list"),
    path("tags/<int:pk>", TagsApiDetail.as_view(), name="tag-detail"),
    path("login/", TokenObtainPairView.as_view()),
]
