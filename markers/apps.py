from django.apps import AppConfig
from django.db.models.signals import post_save

from .signals import add_tags_to_bookmark


class MarkersConfig(AppConfig):
    name = "markers"

    def ready(self):
        bookmark_model = self.get_model("Bookmark")
        post_save.connect(
            add_tags_to_bookmark, sender=bookmark_model, dispatch_uid="add_tags"
        )
