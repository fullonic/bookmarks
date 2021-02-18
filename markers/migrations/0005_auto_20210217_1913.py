# Generated by Django 3.1.4 on 2021-02-17 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('markers', '0004_bookmark_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookmark',
            name='extra_info',
            field=models.CharField(default='', max_length=512),
        ),
        migrations.AlterField(
            model_name='bookmark',
            name='title',
            field=models.CharField(default='', max_length=512),
        ),
    ]
