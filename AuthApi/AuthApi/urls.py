from django.contrib import admin
from django.urls import path,include
from django.urls import re_path
from rest_framework import permissions



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/',include('Auth.urls')),
]