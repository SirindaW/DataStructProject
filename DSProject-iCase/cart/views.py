from django.shortcuts import redirect, render
from .models import Order
from .models import Customer
from django.http import JsonResponse
import json

from product.models import Product
from .models import Order,OrderItem

# Create your views here.

def cart_view(request):
    if request.user.is_authenticated:
        customer,created_customer = Customer.objects.get_or_create(user= request.user,first_name=request.user.first_name,last_name = request.user.last_name,email = request.user.email)
        order,created_order = Order.objects.get_or_create(customer= customer,complete = False)
        items = order.orderitem_set.all() # access all order items in the order

        for item in items:
            item.subtotal_price = round(item.product.price * item.quantity,2)

    else :
        return redirect('login_view')

    print('items len',len(items))
    context = {
        'items':items,
        'order':order,
        'cart_empty':len(items)<=0,
    }
    return render(request,'cart.html',context)

def update_item_view(request):
    data = json.loads(request.body)
    productSlug = data['productSlug']
    quantity = data['quantity']
    action = data['action']

    print(action,productSlug,quantity)
    customer = request.user.customer
    product = Product.objects.get(slug = productSlug)

    order,created = Order.objects.get_or_create(customer = customer,complete = False)
    
    order_item,created = OrderItem.objects.get_or_create(order=order,product=product)

    if action == 'add':
        order_item.quantity = (order_item.quantity + int(quantity))
    elif action == "remove":
        order_item.quantity = 0

    order_item.save()
    print('something')

    if order_item.quantity <= 0:
        order_item.delete()

    return JsonResponse('Item was added.',safe = False)