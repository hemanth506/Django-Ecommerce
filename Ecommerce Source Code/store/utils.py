import json
from . models import *

def cookiecart(resp):
    try:
            cart = json.loads(resp.COOKIES['cart'])
    except:
        cart = {}
    print("cart:",cart)

    items =[]
    order = {"get_cart_quantity":0,"get_cart_total":0,"shipping":False}
    cartItems = order['get_cart_quantity']

    for i in cart:
        try:
            if(cart[i]['quantity']>0): #items with negative quantity = lot of freebies  
                cartItems += cart[i]['quantity']

                product = Product.objects.get(id=i)
                total = (product.price * cart[i]['quantity'])

                order['get_cart_total'] += total
                order['get_cart_quantity'] += cart[i]['quantity']


                item = {
                    'product' :{
                        'id' : product.id,
                        'name':product.name,
                        'price':product.price,
                        'image_url_exists':product.image_url_exists,
                    },
                    'quantity': cart[i]['quantity'],
                    'get_total':total
                }
                items.append(item)

                if product.digital == False:
                    order['shipping'] = True
        except:
            pass

    user = resp.user
    return {"items":items,"order":order,"user":user,"cartItems":cartItems}


def cartdata(resp):
    if resp.user.is_authenticated:
        customer = resp.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_quantity
    else:
        # items = []
        # order = {"get_cart_items": 0, "get_cart_total": 0,"shipping":False}
        # order = {"get_cart_quantity": 0, "get_cart_total": 0,"shipping":False}
        # cartItems = order['get_cart_quantity']
        cookieData = cookiecart(resp)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
        
    user = resp.user
    return {"items":items,"order":order,"user":user,"cartItems":cartItems}


def guestorder(resp, data):
    print("User is not logged in")

    print("cookie :", resp.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookiedata = cookiecart(resp)
    items = cookiedata['items']

    # if the user has no account but uses with the email ,
    # here now it checks if the user's email is already exixts in cookies,if exists it exists or it is created
    customer , created = Customer.objects.get_or_create(
        email = email,
    )

    customer.name = name
    customer.save()

    order , created = Order.objects.get_or_create(
        customer = customer,
        complete = False,
    ) 

    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        orderitem = OrderItem.objects.create(
            product = product,
            order = order , 
            quantity = (item['quantity'] if item['quantity'] > 0 else -1* item['quantity']),

        )
    return customer, order