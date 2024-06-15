from django.contrib import admin
from django.urls import path, include
from app.views import index, product_detail, prod_attr, add_product, customers, customer_detail,add_customer, customer_detail,delete_customer


urlpatterns = [
    path('index/', index, name='index'),
    path('product_details/<int:product_id>', product_detail, name='product_detail'),
    path('prod_attr/<int:product_id>', prod_attr, name='prod_attr'),
    path('add-product/', add_product, name='add_product'),
    path('customers', customers, name='customers'),
    path('add-customer/', add_customer, name='add_customers'),
    path('customer-details/<int:customer_id>', customer_detail, name='customer_detail', ),
    path('delete-customer/<int:customer_id>', delete_customer, name='delete_customer'),
]
