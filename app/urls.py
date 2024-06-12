from django.contrib import admin
from django.urls import path, include
from app.views import index, product_detail, prod_attr

urlpatterns = [
    path('index/', index, name='index'),
    path('product_details/<int:product_id>', product_detail, name='product_detail'),
    path('prod_attr/<int:product_id>', prod_attr, name='prod_attr'),
]
