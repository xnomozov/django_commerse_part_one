from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from app.forms import ProductModelForm
from app.models import Product
from django.views import View


class ProductListView(View):

    def get(self, request):
        page = request.GET.get('page', '')
        products = Product.objects.all().order_by('-id')
        paginator = Paginator(products, 2)
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        context = {
            'page_obj': page_obj
        }
        return render(request, 'app/index.html', context)


class ProductDetailTemplateView(TemplateView):
    template_name = 'app/product-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Product.objects.get(id=kwargs['product_id'])
        context['product'] = product
        context['attributes'] = product.get_attribute()
        return context


def prod_attr(request, product_id):
    product = Product.objects.get(id=product_id)
    attributes = product.attributes_to_list()
    context = {'attributes': attributes, }
    return render(request, 'app/index.html', context)


class AddProductView(View):
    def get(self, request):
        form = ProductModelForm()
        return render(request, 'app/add-product.html', {'form': form})

    def post(self, request):
        form = ProductModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')


class DeleteProduct(View):

    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        product.delete()
        return redirect('index')


class EditProductTemplateView(TemplateView):
    template_name = 'app/update-product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Product.objects.get(id=kwargs['product_id'])
        context['form'] = ProductModelForm(instance=product)
        return context

    def post(self, request,  *args, **kwargs):
        context = self.get_context_data(**kwargs)

        product = get_object_or_404(Product, id=kwargs['product_id'])
        form = ProductModelForm(instance=product, data=request.POST)
        context['form'] = form
        if form.is_valid():
            form.save()
            return redirect('index')
