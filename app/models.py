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


class Images(models.Model):
    image = models.ImageField(upload_to='images', null=True)
    product = models.ForeignKey('app.Product', on_delete=models.CASCADE, related_name='images')
