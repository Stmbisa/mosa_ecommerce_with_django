from django.shortcuts import render, get_object_or_404
from store.models import Product
from category.models import Category

def store(request, category_slug=None):
    category = None
    products = None
    if category_slug != None:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category = category, is_available = True)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available =  True)
        product_count = products.count()
    context =  {
        'products': products,
        'product_count':product_count
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Product.DoesNotExist:
        return 'The product dont exist'
    context={
        'single_product': single_product,
    }
    return render(request, 'store/product_detail.html', context)