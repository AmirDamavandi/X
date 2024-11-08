from django.urls import path
from .views import *


app_name = 'tweets'

urlpatterns = [
    path('hashtags/', Hashtags.as_view(), name='hashtags')
]