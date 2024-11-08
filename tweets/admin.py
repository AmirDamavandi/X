from django.contrib import admin
from .models import *


# Register your models here.


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'tweet', 'status', 'comment', 'quote_tweet',
        'like_count', 'retweet_count', 'view_count',
        'bookmark_count', 'created_at',
    ]


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