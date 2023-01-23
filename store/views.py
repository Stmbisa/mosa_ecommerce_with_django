from django.shortcuts import render, get_object_or_404
from store.models import Product
from category.models import Category
from django.db.models import Q 
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse

def store(request, category_slug=None):
    category = None
    products = None
    if category_slug != None:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category = category, is_available = True)
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available = True).order_by('id')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    context =  {
        'products': paged_products, #instead of taking the products lets take the paged products 
        'product_count':product_count
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Product.DoesNotExist:
        return 'The product dont exist'
    context={
        'single_product': single_product,
        "in_cart": in_cart
    }
    return render(request, 'store/product_detail.html', context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword)| Q(product_name__icontains= keyword)) # fielter treats , as a and 
            product_count = products.count()
        context = {
            'products':products, 
            'product_count':product_count
        }
    return render(request, 'store/store.html', context)