from django.db import models
from django.utils import timezone
import datetime

#TODO: Add image model to deal with favicons related with tags

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
    
    # TODO: Generate tags when saving the new entry
    # TODO: Add function to check providers
    def __str__(self) -> str:
        return f"{self.title}: {self.url}"
