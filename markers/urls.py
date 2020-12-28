from django.urls import path
from .views import BookmarksApiView, TagsApiView, TagsApiDetail

from .custom_claims import TokenObtainPairView

urlpatterns = [
    path("bookmarks", BookmarksApiView.as_view(), name="bookmark-list"),
    path("tags", TagsApiView.as_view(), name="tag-list"),
    path("tags/<int:pk>", TagsApiDetail.as_view(), name="tag-detail"),
    path("login/", TokenObtainPairView.as_view()),
]
