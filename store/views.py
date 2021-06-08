from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from .models import Product, ReviewRating
from category.models import Category
from carts.views import _cart_id
from carts.models import CartItem
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .forms import ReviewForm
from orders.models import OrderProduct
# Create your views here.


def store(request, category_slug=None):
    categories = None
    products = None

    # This will bring products based on category like  http://127.0.0.1:8000/store/t-shirt/
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        # This is will bring us all products based on the upper defined categories
        products = Product.objects.filter(
            category=categories, is_available=True)
        # this code is for 6 products paginator
        paginator = Paginator(products, 1)
        # 127.0.0.1:8000/store/?page = 2 we want to capture the page keyword after question mark by user requesting as get
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    else:
        # All products are displayed in store http://127.0.0.1:8000/store/
        products = Product.objects.all().filter(is_available=True).order_by('id')

        # this code is for 6 products paginator
        paginator = Paginator(products, 3)
        # 127.0.0.1:8000/store/?page = 2 we want to capture the page keyword after question mark by user requesting as get
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)

        product_count = products.count()
    data = {
        'products': paged_products,
        'product_count': product_count,
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
    try:
        # if it is true we will show him submit review button
        orderproduct = OrderProduct.objects.filter(
            user=request.user, product_id=single_product.id).exists()
    except OrderProduct.DoesNotExist:
        orderproduct = None

    # get the review
    reviews = ReviewRating.objects.filter(
        product_id=single_product.id, status=True)
    print(reviews)

    data = {
        'single_product': single_product,
        'in_cart': in_cart,
        'order_product': orderproduct,
    }
    return render(request, 'store/product_detail.html', data)


# 127.0.0.1:8000/store/search/?keyword=aaaaaadhhdhdhhhd
def search(request):
    # checking the keyword   word in url
    if 'keyword' in request.GET:
        # gettting the keyword that user typed
        keyword = request.GET['keyword']
        if keyword:  # if user has typed something then show the products
            products = Product.objects.order_by(
                '-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count
    }
    return render(request, 'store/store.html', context)


def submit_review(request, product_id):
    # store the previous url
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        try:
            # Try is for update
            # check if user exists with product
            reviews = ReviewRating.objects.get(
                user__id=request.user.id, product__id=product_id)

            # We  are passing instance(object) because if user already reviewd then we just update
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(
                request, 'Thank You! Your review has been updated ')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(
                    request, 'Thank You! Your review has been submitted ')
                return redirect(url)
