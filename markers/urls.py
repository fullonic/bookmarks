from django.urls import path
from .views import BookmarksApiView

from .custom_claims import TokenObtainPairView

urlpatterns = [
    path("bookmarks", BookmarksApiView.as_view(), name="bookmarks-list"),
    path("login/", TokenObtainPairView.as_view()),
]
