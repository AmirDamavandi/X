# Generated by Django 5.1 on 2024-11-08 08:37

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PostView',
            new_name='View',
        ),
        migrations.AlterModelOptions(
            name='bookmark',
            options={'verbose_name': 'Bookmark', 'verbose_name_plural': 'Bookmarks'},
        ),
        migrations.AlterModelOptions(
            name='like',
            options={'verbose_name': 'Like', 'verbose_name_plural': 'Likes'},
        ),
        migrations.AlterModelOptions(
            name='retweet',
            options={'verbose_name': 'Retweet', 'verbose_name_plural': 'Retweets'},
        ),
        migrations.AlterModelOptions(
            name='tweet',
            options={'verbose_name': 'Tweet', 'verbose_name_plural': 'Tweets'},
        ),
        migrations.AlterModelOptions(
            name='view',
            options={'verbose_name': 'Post View', 'verbose_name_plural': 'Post Views'},
        ),
    ]