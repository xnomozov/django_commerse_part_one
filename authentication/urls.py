from django.contrib import admin
from django.urls import path, include

from app import admin
from authentication.views import LoginView, logout_page, RegisterView, SendEmailView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_page, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('send-email/', SendEmailView.as_view(), name='send_email'),



]