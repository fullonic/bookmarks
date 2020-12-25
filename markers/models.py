"""Bookmarks models from Firefox bookmarks sqlite db.

command: python manage.py inspectdb > bookmarks/models.py

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

"""
from django.db import models
from django.db.models.fields import CharField


# class Items(models.Model):
#     guid = models.TextField(unique=True)
#     parentguid = models.TextField(
#         db_column="parentGuid", blank=True, null=True
#     )  # Field name made lowercase.
#     servermodified = models.IntegerField(
#         db_column="serverModified"
#     )  # Field name made lowercase.
#     needsmerge = models.BooleanField(
#         db_column="needsMerge"
#     )  # Field name made lowercase.
#     validity = models.IntegerField()
#     isdeleted = models.BooleanField(db_column="isDeleted")  # Field name made lowercase.
#     kind = models.IntegerField()
#     dateadded = models.IntegerField(db_column="dateAdded")  # Field name made lowercase.
#     title = models.TextField(blank=True, null=True)
#     urlid = models.ForeignKey(
#         "Urls", models.DO_NOTHING, db_column="urlId", blank=True, null=True
#     )  # Field name made lowercase.
#     keyword = models.TextField(blank=True, null=True)
#     description = models.TextField(blank=True, null=True)
#     loadinsidebar = models.BooleanField(
#         db_column="loadInSidebar", blank=True, null=True
#     )  # Field name made lowercase.
#     smartbookmarkname = models.TextField(
#         db_column="smartBookmarkName", blank=True, null=True
#     )  # Field name made lowercase.
#     feedurl = models.TextField(
#         db_column="feedURL", blank=True, null=True
#     )  # Field name made lowercase.
#     siteurl = models.TextField(
#         db_column="siteURL", blank=True, null=True
#     )  # Field name made lowercase.

#     class Meta:
#         managed = False
#         db_table = "items"


# class Meta(models.Model):
#     key = models.TextField(primary_key=True)
#     value = models.TextField()  # This field type is a guess.

#     class Meta:
#         managed = False
#         db_table = "meta"


# class SqliteStat1(models.Model):
#     tbl = models.TextField(blank=True, null=True)  # This field type is a guess.
#     idx = models.TextField(blank=True, null=True)  # This field type is a guess.
#     stat = models.TextField(blank=True, null=True)  # This field type is a guess.

#     class Meta:
#         managed = False
#         db_table = "sqlite_stat1"


# class Structure(models.Model):
#     guid = models.TextField()
#     parentguid = models.ForeignKey(
#         Items, models.DO_NOTHING, db_column="parentGuid"
#     )  # Field name made lowercase.
#     position = models.IntegerField()

#     class Meta:
#         managed = False
#         db_table = "structure"


# class Tags(models.Model):
#     itemid = models.OneToOneField(
#         Items,
#         models.DO_NOTHING,
#         db_column="itemId",
#         primary_key=True,
#     )  # Field name made lowercase.
#     tag = models.TextField()

#     class Meta:
#         managed = False
#         db_table = "tags"

#     def __repr__(self) -> str:
#         return self.tag


# class Urls(models.Model):
#     guid = models.TextField()
#     url = models.URLField(unique=False, max_length=512)
#     hash = models.IntegerField()
#     revhost = models.TextField(db_column="revHost")  # Field name made lowercase.

#     class Meta:
#         managed = True
#         db_table = "urls"


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
