from django.db import models
import datetime


def timestamp_now():
    return datetime.datetime.now().timestamp()


class Tag(models.Model):
    name = models.CharField(max_length=256, unique=True)


class Bookmark(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=512)
    created_on = models.FloatField(default=timestamp_now)
    tags = models.ManyToManyField(Tag)


