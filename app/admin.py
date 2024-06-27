from django.contrib import admin

from app.models import Product, Images, AttributeValue, AttributeKey, ProductAttribute, Customers

# Register your models here.
admin.site.register(Product)
admin.site.register(Images)
admin.site.register(AttributeKey)
admin.site.register(AttributeValue)
admin.site.register(ProductAttribute)
admin.site.register(Customers)

@admin.register(Customers)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name','email','phone','billing_address', 'joined']
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
