from django.shortcuts import render


# Create your views here.

def login(request):
    return render(request, 'authentication/login.html')


def logout(request):
    return render(request, 'authentication/logout.html')


def register(request):
    return render(request, 'authentication/register.html')
