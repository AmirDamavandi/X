from django.urls import path
from .views import *
app_name = 'tweets'

urlpatterns = [
    path('home/', Home.as_view(), name='Home'),
    path('like/<int:tweet_id>/', LikeTweetView.as_view(), name='LikeTweetView'),
    path('dislike/<int:tweet_id>/', UnLikeTweetView.as_view(), name='UnLikeTweetView'),
]