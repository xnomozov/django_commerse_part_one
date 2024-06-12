from django.db import models


# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    price = models.FloatField()
    rating = models.FloatField()
    discount = models.FloatField(default=0, null=True)
    quantity = models.IntegerField(default=0, null=True)

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

    def attributes_as_dict(self):
        attributes = self.get_attribute()
        attributes_dict = {}
        for attr in attributes:
            attributes_dict[attr['attribute_key']] = attr['attribute_value']
        return attributes_dict


class Images(models.Model):
    image = models.ImageField(upload_to='images', null=True)
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
