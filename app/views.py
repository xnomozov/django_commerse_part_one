from msilib.schema import ListView

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect

from app.forms import ProductModelForm, CustomerModelForm
# from app.forms import ProductForm
from app.models import Product, Customers


# Create your views here.
def index(request):
    page = request.GET.get('page', '')
    products = Product.objects.all().order_by('-id')
    paginator = Paginator(products, 1)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {'page_obj': page_obj, }

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
    customer = Customers.objects.all()

    if search_query:
        customer = customer.filter(
            Q(name__icontains=search_query) | Q(billing_address__icontains=search_query)
        )

    paginator = Paginator(customer, 1)
    page = request.GET.get('page')

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {'page_obj': page_obj,
               'search_query': search_query,
               'customer': customer}
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
