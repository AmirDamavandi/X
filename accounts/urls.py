from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('', x, name='x'),
    path('sign-up/', sign_up, name='sign_up'),
]
