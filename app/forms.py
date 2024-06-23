from django import forms

from app.models import Product, Customers, CustomUser


# class ProductForm(forms.Form):
#     name = forms.CharField(max_length=120)
#     description = forms.CharField(widget=forms.Textarea)
#     rating = forms.FloatField()
#     price = forms.FloatField()
#     discount = forms.FloatField()
#     quantity = forms.IntegerField()


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        # fields = '__all__'
        exclude = ()


class CustomerModelForm(forms.ModelForm):
    class Meta:
        model = Customers
        exclude = ()







