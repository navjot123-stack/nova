from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models

class products(models.Model):
    name=models.CharField(max_length=50)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    image=models.ImageField(upload_to='images/')


class CartItem(models.Model):
    product = models.ForeignKey(products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)




class Order(models.Model):
    PAYMENT_CHOICES = [
        ('online', 'Online Payment'),
        ('upi', 'UPI'),
        ('cod', 'Cash on Delivery'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    emailaddress = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)
    country = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip = models.CharField(max_length=20)

    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='cod')
    card_number = models.CharField(max_length=20, blank=True, null=True)
    expiry_date = models.CharField(max_length=10, blank=True, null=True)
    cvv = models.CharField(max_length=5, blank=True, null=True)
    upi_id = models.CharField(max_length=100, blank=True, null=True)

    line_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order #{self.id} by {self.firstname} {self.lastname}"

class cnt(models.Model):
    name=models.CharField(max_length=50)
    lastname=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    message=models.CharField(max_length=50)



class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    cart_item = models.ForeignKey('CartItem', on_delete=models.CASCADE)  # assuming CartItem has product & quantity
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cart_item.product.name} x {self.quantity}"
