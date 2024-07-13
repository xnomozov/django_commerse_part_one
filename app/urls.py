from django.urls import path
from app.views.app.views import DeleteProduct, ProductDetailTemplateView, AddProductView, ProductListView, EditProductTemplateView
from app.views.customers.views import CustomerDetailView, CustomersTemplateView, \
    EditCustomerView, DeleteCustomerView, AddCustomerView, export_data

urlpatterns = [
    path('index/', ProductListView.as_view(), name='index'),
    path('product_details/<int:product_id>', ProductDetailTemplateView.as_view(), name='product_detail'),
    path('add-product/', AddProductView.as_view(), name='add_product'),
    path('customers/', CustomersTemplateView.as_view(), name='customers'),
    path('add-customer/', AddCustomerView.as_view(), name='add_customers'),
    path('customer-details/<int:customer_id>', CustomerDetailView.as_view(), name='customer_detail', ),
    path('delete-customer/<int:customer_id>', DeleteCustomerView.as_view(), name='delete_customer'),
    path('edit_customer/<int:customer_id>', EditCustomerView.as_view(), name='edit_customer'),
    path('export_data/', export_data, name='export_data'),
    path('delete-product/<int:product_id>', DeleteProduct.as_view(), name='delete_product'),
    path('edit-product/<int:product_id>', EditProductTemplateView.as_view(), name='edit_product'),
]
