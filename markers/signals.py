from .core import generate_tags

from django.db.utils import IntegrityError


def add_tags_to_bookmark(sender, instance, **kwargs):
    from .models import Tag

    tag_list = Tag.objects.values_list("name", flat=True)
    tags = generate_tags(instance.url, instance.title, tag_list)
    for t in tags:
        # Create or get tag object
        try:
            tag = Tag.objects.get(name=t)
        except Exception as e:
            Tag.objects.create(name=t)
            tag = Tag.objects.get(name=t)
        finally:
            instance.tags.add(tag)
