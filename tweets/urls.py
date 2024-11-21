from django.urls import path
from .views import *
app_name = 'tweets'

urlpatterns = [
    path('home/', Home.as_view(), name='Home'),
    path('like/<int:tweet_id>/', LikeTweetView.as_view(), name='LikeTweetView'),
    path('dislike/<int:tweet_id>/', UnLikeTweetView.as_view(), name='UnLikeTweetView'),
    path('retweet/<int:tweet_id>/', RetweetView.as_view(), name='RetweetView'),
    path('undoretweet/<int:tweet_id>/', UndoRetweetView.as_view(), name='UndoRetweetView'),
]