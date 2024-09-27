from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('', X.as_view(), name='X'),
    path('sign-up/', SignUpView.as_view(), name='SignUpView'),
    path('login/', LoginView.as_view(), name='LoginView'),
    path('<str:username>/', ProfileView.as_view(), name='ProfileView'),
    path('follow/<str:username>/', FollowView.as_view(), name='FollowView'),
]
