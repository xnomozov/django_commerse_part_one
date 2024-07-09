from django.contrib import admin
from django.utils.safestring import mark_safe

from app.forms import CustomUserModelForm
from app.models import Product, Images, AttributeValue, AttributeKey, ProductAttribute, Customers, CustomUser

# Register your models here.
# admin.site.register(Product)
# admin.site.register(Images)
admin.site.register(AttributeKey)
admin.site.register(AttributeValue)
admin.site.register(ProductAttribute)


# admin.site.register(CustomUser)
# admin.site.register(Customers)
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'username', 'is_staff', 'is_superuser', 'is_active')
    form = CustomUserModelForm


@admin.register(Customers)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'is_active']
    search_fields = ['name', 'email', 'id']
    list_filter = ['joined', 'is_active']


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'rating', 'quantity']
    search_fields = ['name', 'price', 'rating']
    list_filter = ['price', 'rating']


@admin.register(Images)
class ImagesModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'product']
    search_fields = ['product']
