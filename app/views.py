from msilib.schema import ListView

from django.db.models import Q
from django.shortcuts import render, redirect

from app.forms import ProductModelForm, CustomerModelForm
# from app.forms import ProductForm
from app.models import Product, Customers


# Create your views here.
def index(request):
    products = Product.objects.all().order_by('-id')
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


# def add_product(request):
#     # form = ProductForm()
#     if request.method == 'POST':
#         form = ProductForm(request.POST)
#         name = request.POST['name']
#         price = request.POST['price']
#         rating = request.POST['rating']
#         description = request.POST['description']
#         discount = request.POST['discount']
#         quantity = request.POST['quantity']
#         product = Product(name=name, price=price, description=description, quantity=quantity, discount=discount,
#                           rating=rating)
#         if form.is_valid():
#             product.save()
#             return redirect('index')
#     else:
#         form = ProductForm()
#
#     context = {'form': form}
#     return render(request, 'app/add-product.html', context)


def add_product(request):
    form = ProductModelForm()
    if request.method == 'POST':
        form = ProductModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    context = {'form': form}
    return render(request, 'app/add-product.html', context)


def customers(request):
    search_query = request.GET.get('search')
    if search_query:
        customer = Customers.objects.filter(
            Q(name__icontains=search_query) | Q(billing_address__icontains=search_query))
    else:
        customer = Customers.objects.all()
    context = {'customers': customer}
    return render(request, 'app/customers.html', context)


def customer_detail(request, customer_id):
    customer = Customers.objects.get(id=customer_id)
    context = {'customer': customer}
    return render(request, 'app/customer-details.html', context)


def add_customer(request):
    form = CustomerModelForm()
    if request.method == 'POST':
        form = CustomerModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customers')
    context = {'form': form}
    return render(request, 'app/add-customer.html', context)


def delete_customer(request, customer_id):
    customer = Customers.objects.get(id=customer_id)
    customer.delete()
    return redirect("customers")


def edit_customer(request, customer_id):
    customer = Customers.objects.get(id=customer_id)
    form = CustomerModelForm(instance=customer)
    if request.method == 'POST':
        form = CustomerModelForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect("customers")
    context = {
        'form': form,
    }
    return render(request, 'app/update-customer.html', context)
