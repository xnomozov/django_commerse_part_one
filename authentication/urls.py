
from django.urls import path
from authentication import views
from authentication.views import  logout_page, SendEmailView

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('register/', views.register_page, name='register'),
    path('send-email/', SendEmailView.as_view(), name='send_email'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate')

]
