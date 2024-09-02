from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('', x, name='x'),
    path('sign-up/', sign_up, name='sign_up'),
    path('sign-in/', sign_in, name='sign_in'),
]
