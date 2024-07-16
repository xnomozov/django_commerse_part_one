from django.contrib.admin import register
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from app.models import CustomUser
from authentication.forms import LoginForm, RegisterForm, EmailForm


# Create your views here.

# def login_page(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             phone_number = form.cleaned_data['phone_number']
#             password = form.cleaned_data['password']
#             user = authenticate(request, phone_number=phone_number, password=password)
#             if user:
#                 login(request, user)
#                 return redirect('customers')
#     else:
#         form = LoginForm()
#
#     return render(request, 'authentication/login.html', {'form': form})

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        context = {'form': form}
        return render(request, 'authentication/login.html', context)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            user = authenticate(request, phone_number=phone_number, password=password)
            if user:
                login(request, user)
                return redirect('customers')


def logout_page(request):
    logout(request)
    return render(request, 'authentication/logout.html')


# def register_page(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             phone_number = form.cleaned_data['phone_number']
#             password = form.cleaned_data['password']
#
#             user = CustomUser.objects.create_user(username=username, phone_number=phone_number, password=password)
#             login(request, user)
#             return redirect('customers')
#
#     else:
#         form = RegisterForm()
#
#     return render(request, 'authentication/register.html', {'form': form})

class RegisterView(FormView):
    template_name = 'authentication/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('customers')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        return super().form_valid(form)


class SendEmailView(View):
    def get(self, request):
        form = EmailForm()
        context = {'form': form}
        return render(request, 'app/send-email.html', context)

    def post(self, request):
        form = EmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            email_from = form.cleaned_data['email_from']
            email_to = [form.cleaned_data['email_to']]
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, email_from, email_to)
                messages.success(request, 'Message sent successfully.')
                return redirect('customers')
            except Exception as e:
                messages.error(request, f'Error sending message: {e}')

        context = {'form': form}
        return render(request, 'app/send-email.html', context)
