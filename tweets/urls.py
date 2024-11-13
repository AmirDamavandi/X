from django.urls import path
from .views import *
app_name = 'tweets'

urlpatterns = [
    path('home/', Home.as_view(), name='Home'),
]