from markers.core import extract_icon_from_url, get_extra_info
from django.db import models, transaction
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
    title = models.CharField(max_length=512, default="")
    extra_info = models.CharField(max_length=512, default="")
    created_on = models.FloatField(default=timestamp_now)
    last_time_visited = models.DateTimeField(
        default=timezone.now, blank=True, null=True
    )
    tags = models.ManyToManyField(Tag)
    icon = models.URLField(default="")

    @transaction.atomic
    def save(self, **kwargs) -> None:
        if self._state.adding:
            self.icon = extract_icon_from_url(self.url)
            transaction.on_commit(lambda: write_extra_info_to_table(pk=self.pk))
        return super().save(**kwargs)

    def __str__(self) -> str:
        return f"{self.title}: {self.url}"


def write_extra_info_to_table(pk):
    # TODO: Transform this function to a background job
    book = Bookmark.objects.get(pk=pk)
    print(f">> Fetching extra information from {book.url}")
    extra_info = get_extra_info(book.url)
    book.extra_info = extra_info
    book.save()
    return book
