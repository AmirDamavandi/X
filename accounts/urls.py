from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('', X.as_view(), name='X'),
    path('sign-up/', SignUpView.as_view(), name='SignUpView'),
    path('sign-in/', sign_in, name='sign_in'),
]
