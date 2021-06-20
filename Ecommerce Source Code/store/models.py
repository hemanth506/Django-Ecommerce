from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# if the user item is deleted the data in db also "deletes" with "on_delete=models.CASCADE"

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=7,decimal_places=2)
    digital = models.BooleanField(default=False,null=True,blank=True)
    image = models.ImageField(null=True,blank=True)
    def __str__(self):
        return self.name

    @property
    def image_url_exists(self):
        try:
            # print("Hemanth")
            url =self.image.url
        except:
            # print("in except")
            url = ""
        return url

# "customer" object holds the foreignkey for "Customer" Class
# if the user item is deleted the data in db sets to "null" with "on_delete=models.SET_NULL"
# can change the order whenever it is changed "auto_now_add=True"
# returning id refers to default database id with is returned as string "str(self.id)"
class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200,null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for item in orderitems:
            if item.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitem = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitem])
        return total

    @property
    def get_cart_quantity(self):
        orderitem = self.orderitem_set.all()
        quantity = sum([item.quantity for item in orderitem])
        return quantity


# "product" object holds the foreignkey for "Product" Class
# "order" object holds the foreignkey for "Order" Class
class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    address = models.CharField(max_length=200,null=False)
    city = models.CharField(max_length=200,null=False)
    state = models.CharField(max_length=200,null=False)
    zip_code = models.CharField(max_length=200,null=False)
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.address)


