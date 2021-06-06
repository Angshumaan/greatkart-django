from django.http.response import HttpResponse
from django.shortcuts import redirect, render, HttpResponse
from carts.models import CartItem
from .forms import OrderForm
from .models import Order, OrderProduct, Payment
import datetime
import json
# Create your views here.


def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(
        user=request.user, is_ordered=False, order_number=body['orderID'])
    print(body)

    # store transaction details inside payment model from javascript fetch
    payment = Payment(
        user=request.user,
        payment_id=body['transID'],
        payment_method=body['payment_method'],
        amount_paid=order.order_total,
        status=body['status'],
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    # move the cart items to order product table(model)
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

    # reduce the quantity of sold products

    # clear the cart

    # send order received email to the customer

    # send order number and transaction id back to  sendData method via JsonResponse
    return render(request, 'orders/payments.html')


def place_order(request, total=0, quantity=0):
    # we are loggedd in so we can ask user everywhere
    current_user = request.user

    # if the cart count is less than or equal to 0 then redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price*cart_item.quantity)
        quantity += cart_item.quantity
        print('Total:- ', total)
        print('Quantity:- ', quantity)

    tax = (2*total)/100
    grand_total = total+tax

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            # store all the valid information inside order table
            data = Order()  # Instance of order

            # extract using data.first_name ..data is an object  and we got all the data from the instance
            # Bring it from html name that is we get from request.post using form.cleaned_data
            data.user = current_user
            data.first_name = form.cleaned_data["first_name"]
            data.last_name = form.cleaned_data["last_name"]
            data.phone = form.cleaned_data["phone"]
            data.email = form.cleaned_data["email"]
            data.address_line_1 = form.cleaned_data["address_line_1"]
            data.address_line_2 = form.cleaned_data["address_line_2"]
            data.country = form.cleaned_data["country"]
            data.state = form.cleaned_data["state"]
            data.city = form.cleaned_data["city"]
            data.order_note = form.cleaned_data["order_note"]
            data.order_total = grand_total  # we are getting it from above code
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")  # 20210305
            # concatenating current date with primary key
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            # we are going to make it true when payment is success
            order = Order.objects.get(
                user=current_user, is_ordered=False, order_number=order_number)
            print(order)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }
            return render(request, 'orders/payments.html', context)
        else:
            return redirect('checkout')
