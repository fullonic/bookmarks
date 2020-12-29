from django.db import models
from django.utils import timezone
import datetime


def timestamp_now():
    return datetime.datetime.now().timestamp()


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

    def __str__(self) -> str:
        return f"{self.title}: {self.url}"
