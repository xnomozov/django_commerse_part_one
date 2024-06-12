from django.shortcuts import render

from app.models import Product


# Create your views here.
def index(request):
    products = Product.objects.all()
    context = {'products': products}

    return render(request, 'app/index.html', context)


def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    attributes = product.get_attribute()
    context = {'product': product,
               'attributes': attributes}
    return render(request, 'app/product-details.html', context)


def prod_attr(request, product_id):
    product = Product.objects.get(id=product_id)
    attributes = product.attributes_to_list()
    context = {'attributes': attributes, }
    return render(request, 'app/index.html', context)
