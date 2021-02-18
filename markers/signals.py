from .core import generate_tags

from django.db.utils import IntegrityError

# TODO: Remove Signals: Move this for a normal function to be call when saving a new bookmark
def add_tags_to_bookmark(sender, instance, **kwargs):
    from .models import Tag

    tag_list = Tag.objects.values_list("name", flat=True)
    tags = generate_tags(instance.url, instance.title, tag_list)
    for t in tags:
        tag = Tag.objects.get(name=t)
        instance.tags.add(tag)
