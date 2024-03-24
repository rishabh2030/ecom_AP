from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserRegisterAPI.as_view(), name='register'),
    path('login/', UserLoginAPI.as_view(), name='login'),
]