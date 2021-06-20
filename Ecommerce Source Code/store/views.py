from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import json
import datetime
from .utils import cookiecart , cartdata , guestorder

# Create your views here.

def store(resp):
    # print(resp.user)
    data = cartdata(resp)
    cartItems = data['cartItems']

    products = Product.objects.all()
    user = resp.user
    # content = {'products':products,"user":user,"cartItems":cartItems,"shipping":False}
    content = {'products':products,"user":user,"cartItems":cartItems}
    return render(resp,"store/store.html", content)

""" 
go_or_create :
The trick with the get_or_create method is that it actually returns a tuple of (object, created).
 The first element is an instance of the model you are trying to retrieve and 
  the second is a boolean flag to tell if the instance was created or not.
   True means the instance was created by the get_or_create method and
    False means it was retrieved from the database.
"""
"""
customer = resp.user.customer :
  one_to_one relation with django user and customer class which is created in models.py
"""
def cart(resp):
    data = cartdata(resp)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    user = resp.user
    content = {"items":items,"order":order,"user":user,"cartItems":cartItems}
    return render(resp,"store/cart.html", content)

# Here, cart function and checkout function has same functionality
def checkout(resp):
    data = cartdata(resp)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    user = resp.user
    content = {"items": items, "order": order,"user":user,"cartItems":cartItems}
    return render(resp, "store/checkout.html",content)

# to get updated items from json file
def update_item(resp):
    data = json.loads(resp.body)
    productId = data['productId']
    action = data['action']
    print(productId,"  ",action)

    customer = resp.user.customer
    product = Product.objects.get(id=productId)

    # to check if the order is placed by the customer who have'nt completed shopping(False)
    # and , order is the return item
    order , created = Order.objects.get_or_create(customer=customer,complete=False)

    # to check if the item already exists in the order by the customer
    orderedItem , created = OrderItem.objects.get_or_create(order=order,product=product)

    if action == 'add':
        orderedItem.quantity = (orderedItem.quantity+1)
    elif action == 'remove':
        orderedItem.quantity = (orderedItem.quantity - 1)

    orderedItem.save()

    if orderedItem.quantity <= 0:
        orderedItem.delete()

    return JsonResponse("items are updated",safe=False)


def process_order(resp):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(resp.body)

    # login user
    if resp.user.is_authenticated:
        customer = resp.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    # guest user
    else:
        customer , order = guestorder(resp, data)

    # both users can place orders
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    # if total == float(order.get_cart_total):
    if total == order.get_cart_total:
        order.complete = True
        
    order.save()

    # create shipping address values (models.url)
    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zip_code = data['shipping']['zip_code']
        )

    return JsonResponse("Payment transferred..", safe=False)