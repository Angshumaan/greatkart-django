from typing import Hashable
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Variation
from .models import Cart, CartItem
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
# Create your views here.

# session id  that will be cart id private,,, checking from request in django


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    '''gettign the product here'''
    product = Product.objects.get(
        id=product_id)  # checking product_id that the user is giving with the database id
    '''product variation here'''
    product_variation = []
    if request.method == 'POST':
        # Just like dictionary if we wnat key adn value
        for item in request.POST:
            key = item
            value = request.POST[key]
            try:
                variation = Variation.objects.get(
                    product=product, variation_category__iexact=key, variation_value__iexact=value)
                # now we can store this to cartItem go to cart models and make a field and store in cartItem
                product_variation.append(variation)
                print('haa', product_variation)
            except:
                pass
    try:
        '''Cart id here'''
        # checking cart_id that with the _cart_id function that matches in datbase
        # get the cart using the cart_id present in the session
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
        cart.save()

    is_cart_item_exists = CartItem.objects.filter(
        product=product, cart=cart)

    if is_cart_item_exists:
        cart_item = CartItem.objects.filter(
            product=product, cart=cart)
        # existing variation -> databse
        # current variation -> product variation
        # item id -> database
        # if current variation from user is inside the database that is existing variation then we just need to incerease the variation
        existing_var_list = []
        id = []
        for item in cart_item:
            existing_variation = item.variations.all()
            existing_var_list.append(list(existing_variation))
            id.append(item.id)
            print(existing_var_list)

        if product_variation in existing_var_list:
            # increase the cart item quantity
            index = existing_var_list.index(product_variation)
            item_id = id[index]
            print('index', item_id)
            item = CartItem.objects.get(product=product, id=item_id)
            print('item', item)
            item.quantity += 1
            item.save()

        else:
            # create a new cart item
            item = CartItem.objects.create(
                product=product, quantity=1, cart=cart)
            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)
            item.save()
    else:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )
        if len(product_variation) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)
        cart_item.save()

    # return HttpResponse(cart_item.product)
    # exit()
    return redirect('cart')

# for - minus href quantity


def remove_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    print('Cart id :', cart)
    product = get_object_or_404(Product, id=product_id)
    print('Product :', product)
    try:
        cart_item = CartItem.objects.get(
            product=product, cart=cart, id=cart_item_id)
        print('cart_item:', cart_item)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')
# cart page where payments reside


def remove_cart_item(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(
        product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        # we coould initialize in up cart function like total = 0
        tax = 0
        grand_total = 0
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price*cart_item.quantity)
            quantity += cart_item.quantity

        tax = (2*total)/100
        grand_total = total+tax

    except ObjectDoesNotExist:
        pass
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total
    }

    return render(request, 'store/cart.html', context)


@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        # we coould initialize in up cart function like total = 0
        tax = 0
        grand_total = 0
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price*cart_item.quantity)
            quantity += cart_item.quantity

        tax = (2*total)/100
        grand_total = total+tax

    except ObjectDoesNotExist:
        pass
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total
    }
    return render(request, 'store/checkout.html', context)
