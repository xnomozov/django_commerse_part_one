from django.contrib import admin
from django.urls import path, include

from app import admin
from authentication.views import login, logout, register

urlpatterns = [
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('register', register, name='register'),


]