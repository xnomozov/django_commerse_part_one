from django.contrib import admin
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from app.forms import CustomUserModelForm
from app.models import Product, Images, AttributeValue, AttributeKey, ProductAttribute, Customers, CustomUser
from adminsortable2.admin import SortableAdminMixin

admin.site.register(AttributeKey)
admin.site.register(AttributeValue)
admin.site.register(ProductAttribute)


# admin.site.register(CustomUser)
# admin.site.register(Customers)
class CustomUserResource(resources.ModelResource):
    class Meta:
        model = CustomUser
        fields = ('phone_number', 'username', 'birth_of_date', 'is_active', 'is_staff', 'is_superuser',)


@admin.register(CustomUser)
class CustomUserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = CustomUserResource

    list_display = ('username', 'phone_number', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser')
    search_fields = ('username', 'phone_number')
    form = CustomUserModelForm


@admin.register(Customers)
class CustomerModelAdmin(SortableAdminMixin, ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'is_active']
    search_fields = ['name', 'email', 'id']
    list_filter = ['joined', 'is_active']



@admin.register(Product)
class ProductModelAdmin(SortableAdminMixin, ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'rating', 'quantity']
    search_fields = ['name', 'price', 'rating']
    list_filter = ['price', 'rating']


@admin.register(Images)
class ImagesModelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'image', 'product']
    search_fields = ['product']
