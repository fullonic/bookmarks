# Generated by Django 3.1.4 on 2020-12-21 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guid', models.TextField(unique=True)),
                ('parentguid', models.TextField(blank=True, db_column='parentGuid', null=True)),
                ('servermodified', models.IntegerField(db_column='serverModified')),
                ('needsmerge', models.BooleanField(db_column='needsMerge')),
                ('validity', models.IntegerField()),
                ('isdeleted', models.BooleanField(db_column='isDeleted')),
                ('kind', models.IntegerField()),
                ('dateadded', models.IntegerField(db_column='dateAdded')),
                ('title', models.TextField(blank=True, null=True)),
                ('keyword', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('loadinsidebar', models.BooleanField(blank=True, db_column='loadInSidebar', null=True)),
                ('smartbookmarkname', models.TextField(blank=True, db_column='smartBookmarkName', null=True)),
                ('feedurl', models.TextField(blank=True, db_column='feedURL', null=True)),
                ('siteurl', models.TextField(blank=True, db_column='siteURL', null=True)),
            ],
            options={
                'db_table': 'items',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Meta',
            fields=[
                ('key', models.TextField(primary_key=True, serialize=False)),
                ('value', models.TextField()),
            ],
            options={
                'db_table': 'meta',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SqliteStat1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tbl', models.TextField(blank=True, null=True)),
                ('idx', models.TextField(blank=True, null=True)),
                ('stat', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'sqlite_stat1',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Structure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guid', models.TextField()),
                ('position', models.IntegerField()),
            ],
            options={
                'db_table': 'structure',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.TextField()),
            ],
            options={
                'db_table': 'tags',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Urls',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guid', models.TextField()),
                ('url', models.TextField()),
                ('hash', models.IntegerField()),
                ('revhost', models.TextField(db_column='revHost')),
            ],
            options={
                'db_table': 'urls',
                'managed': False,
            },
        ),
    ]
