from markers.core import extract_icon_from_url
from django.db import models
from django.utils import timezone
import datetime


def timestamp_now():
    return datetime.datetime.utcnow().timestamp()


class Stats(models.Model):
    bookmark = models.ForeignKey("Bookmark", on_delete=models.CASCADE)
    times_visited = models.SmallIntegerField(default=0)


class Tag(models.Model):
    name = models.CharField(max_length=256, unique=True)


class Bookmark(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=512)
    created_on = models.FloatField(default=timestamp_now)
    last_time_visited = models.DateTimeField(
        default=timezone.now, blank=True, null=True
    )
    tags = models.ManyToManyField(Tag)
    icon = models.URLField(default="")
    # TODO: Generate tags when saving the new entry
    # TODO: Add function to check providers
    def save(self, **kwargs) -> None:
        if self._state.adding:
            self.icon = extract_icon_from_url(self.url)
        return super().save(**kwargs)

    def __str__(self) -> str:
        return f"{self.title}: {self.url}"
