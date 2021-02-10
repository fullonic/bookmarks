from django.contrib import admin

from .models import Bookmark, Tag

# admin.site.register(, Tag)


@admin.register(Bookmark)
class BookmarkersAdmin(admin.ModelAdmin):
    ...
