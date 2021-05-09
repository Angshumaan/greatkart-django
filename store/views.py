from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from carts.views import _cart_id
from carts.models import CartItem
from django.http import HttpResponse
# Create your views here.


def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        # This is will bring us all products based on the upper defined categories
        products = Product.objects.filter(
            category=categories, is_available=True)
        product_count = products.count()

    else:
        products = Product.objects.all().filter(is_available=True)
        product_count = products.count()
    data = {
        'products': products,
        'product_count': product_count
    }
    return render(request, 'store/store.html', data)


def product_detail(request, category_slug, product_slug):
    try:
        # first we need to get access the category,category__slug is from model category and slug is from product  eg:http://127.0.0.1:8000/store/t-shirt/great-tshirt/
        single_product = Product.objects.get(
            category__slug=category_slug, slug=product_slug)
        # It is a foreign key so we will acces cart attribute(column)from CartItem and inside it i want to acces cart_id from Cart
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(
            request), product=single_product).exists()
        # if product  exists in cart then it will return true or else false
        # return HttpResponse('in_cart')
    except Exception as e:
        raise e

    data = {
        'single_product': single_product,
        'in_cart': in_cart,
    }
    return render(request, 'store/product_detail.html', data)
