import csv
import json
from django.apps import apps
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

from openpyxl import Workbook
from app.forms import CustomerModelForm
from app.models import Product, Customers
from django.views.generic import TemplateView, DetailView


# def customers(request):
#     search_query = request.GET.get('search')
#     customer = Customers.objects.all()
#
#     if search_query:
#         customer = customer.filter(
#             Q(name__icontains=search_query) | Q(billing_address__icontains=search_query)
#         )
#
#     paginator = Paginator(customer, 5)
#     page = request.GET.get('page')
#
#     try:
#         page_obj = paginator.page(page)
#     except PageNotAnInteger:
#         page_obj = paginator.page(1)
#     except EmptyPage:
#         page_obj = paginator.page(paginator.num_pages)
#
#     context = {'page_obj': page_obj,
#                'search_query': search_query,
#                'customer': customer}
#     return render(request, 'app/customers.html', context)

class CustomersTemplateView(TemplateView):
    template_name = 'app/customers.html'

    def get_context_data(self, **kwargs):
        customer = Customers.objects.all()
        search_query = self.request.GET.get('search')
        if search_query:
            customer = customer.filter(
                Q(name__icontains=search_query) | Q(billing_address__icontains=search_query)
            )

        context = super().get_context_data(**kwargs)
        page = self.request.GET.get('page')
        paginator = Paginator(customer, 5)

        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        context['page_obj'] = page_obj
        context['customer'] = customer
        context['search_query'] = search_query
        return context


# def customer_detail(request, customer_id):
#     customer = Customers.objects.get(id=customer_id)
#     context = {'customer': customer}
#     return render(request, 'app/customer-details.html', context)


class CustomerDetailView(TemplateView):
    template_name = 'app/customer-details.html'

    def get_context_data(self, **kwargs):
        customer = Customers.objects.get(id=self.kwargs['customer_id'])
        context = super().get_context_data(**kwargs)
        context['customer'] = customer
        return context


# def add_customer(request):
#     form = CustomerModelForm()
#     if request.method == 'POST':
#         form = CustomerModelForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('customers')
#     context = {'form': form}
#     return render(request, 'app/add-customer.html', context)


class AddCustomerView(TemplateView):
    template_name = 'app/add-customer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CustomerModelForm()
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        form = CustomerModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('customers')


# def delete_customer(request, customer_id):
#     customer = Customers.objects.get(id=customer_id)
#     customer.delete()
#     return redirect("customers")


class DeleteCustomerView(TemplateView):

    def get(self, request, *args, **kwargs):
        customer = Customers.objects.get(id=self.kwargs['customer_id'])
        customer.delete()
        return redirect("customers")


# def edit_customer(request, customer_id):
#     customer = Customers.objects.get(id=customer_id)
#     form = CustomerModelForm(instance=customer)
#     if request.method == 'POST':
#         form = CustomerModelForm(request.POST, instance=customer)
#         if form.is_valid():
#             form.save()
#             return redirect("customers")
#     context = {
#         'form': form,
#     }
#     return render(request, 'app/update-customer.html', context)


class EditCustomerView(TemplateView):
    template_name = 'app/update-customer.html'

    def get_context_data(self, **kwargs):
        form = CustomerModelForm(instance=Customers.objects.get(id=self.kwargs['customer_id']))
        context = super().get_context_data(**kwargs)
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        customer = Customers.objects.get(id=self.kwargs['customer_id'])
        form = CustomerModelForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect("customers")

        context = self.get_context_data(**kwargs)
        context['form'] = form
        return context


def export_data(request):
    format_type = request.GET.get('format', 'csv')
    model = apps.get_model(app_label='app', model_name='Customers')

    if format_type == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=customers.csv'

        writer = csv.writer(response)
        writer.writerow([field.name for field in model._meta.fields])

        for obj in model.objects.all().values_list():
            writer.writerow(obj)
    elif format_type == 'json':
        response = HttpResponse(content_type='application/json')
        data = list(model.objects.all().values('name', 'email', 'phone', 'billing_address'))
        response.write(json.dumps(data, indent=4))
        response['Content-Disposition'] = 'attachment; filename=customers.json'

    elif format_type == 'xlsx':
        response = HttpResponse(content_type='application/vnd.ms-excel')

        wb = Workbook()
        ws = wb.active
        ws.title = 'Customers'
        ws.append(['Name', 'Email', 'Phone', 'Billing Address'])
        for obj in model.objects.all().values_list('name', 'email', 'phone', 'billing_address'):
            ws.append(obj)
        wb.save(response)
        response['Content-Disposition'] = 'attachment; filename=customers.xlsx'
    else:
        response = HttpResponse(status=404)
        response.content = 'Bad request'

    return response
