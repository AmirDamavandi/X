from django.contrib import admin
from django.contrib.admin import TabularInline

from .models import *


# Register your models here.

class HashtagTabularAdmin(TabularInline):
    model = Hashtag


class MediaTabularAdmin(TabularInline):
    model = Media


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'tweet', 'status', 'comment', 'quote_tweet',
        'like_count', 'retweet_count', 'view_count',
        'bookmark_count', 'created_at',
    ]
    inlines = [HashtagTabularAdmin, MediaTabularAdmin]


@admin.register(View)
class PostViewAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'tweet', 'created_at',
    ]

@admin.register(Retweet)
class RetweetAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'tweet', 'created_at',
    ]

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'tweet', 'created_at',
    ]


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'tweet', 'created_at',
    ]

@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display = ['tweet', 'hashtag', 'created_at']

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ['tweet', 'media', 'created_at']