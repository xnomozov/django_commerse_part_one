from django.shortcuts import render

from app.models import Product


# Create your views here.
def index(request):
    products = Product.objects.all()
    context = {'products': products,
               }

    return render(request, 'app/index.html', context)
