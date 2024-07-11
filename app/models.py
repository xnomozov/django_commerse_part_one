from adminsortable2.admin import SortableAdminMixin

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from app.managers import CustomUserManager


# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    price = models.FloatField()
    rating = models.FloatField(default=0)
    discount = models.FloatField(default=0, null=True)
    quantity = models.IntegerField(default=0, null=True)
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    class Meta:
        ordering = ('order',)

    @property
    def discounted_price(self):
        if self.discount > 0:
            return self.price * (1 - self.discount / 100)
        return self.price

    def __str__(self):
        return self.name

    def get_attribute(self):
        product_attribute = ProductAttribute.objects.filter(product=self)
        attributes = []
        for prod_at in product_attribute:
            attributes.append({
                'attribute_key': prod_at.key,
                'attribute_value': prod_at.value
            })
        return attributes

    @property
    def get_attributes_as_dict(self) -> dict:
        attributes = self.get_attribute()
        attributes_dict = {}
        for attribute in attributes:
            attributes_dict[attribute['attribute_key']] = attribute['attribute_value']

        return attributes_dict


class Images(models.Model):
    image = models.ImageField(upload_to='images', blank=True, null=True)
    product = models.ForeignKey('app.Product', on_delete=models.CASCADE, related_name='images')


class AttributeKey(models.Model):
    key = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.key


class AttributeValue(models.Model):
    value = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.value


class ProductAttribute(models.Model):
    product = models.ForeignKey('app.Product', on_delete=models.CASCADE)
    key = models.ForeignKey('app.AttributeKey', on_delete=models.CASCADE)
    value = models.ForeignKey('app.AttributeValue', on_delete=models.CASCADE)


class Customers(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.IntegerField()
    billing_address = models.CharField(max_length=500)
    joined = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    class Meta:
        ordering = ('order',)
        verbose_name = 'Customers'

    def __str__(self):
        return f'{self.name} - {self.joined}'


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = models.IntegerField(unique=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    birth_of_date = models.DateField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.password

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
            self.password = make_password(self.password)

        super().save(*args, **kwargs)
