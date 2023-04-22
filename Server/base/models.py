from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings






class CustomUser(AbstractUser):

    location = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=20)
    image = models.ImageField(upload_to='user_images', null=True, blank=True)


   

class Category(models.Model):
    category_name = models.CharField(max_length=50)
    


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    specification = models.TextField()
    image = models.ImageField(upload_to='product_images', null=True, blank=True)

    def __str__(self):
        return self.product_name

# class Order(models.Model):
#     DELIVERY_OPTIONS = (
#         ('Online', 'Khalti'),
#         ('Cash on delivery', 'Cash on delivery')
#     )

#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     delivery_address = models.CharField(max_length=250)
#     is_paid = models.BooleanField(default=False)
#     delivery_option = models.CharField(max_length=20, choices=DELIVERY_OPTIONS, default='standard')

class Order(models.Model):
    delivery_address = models.CharField(max_length=250)
    is_paid = models.BooleanField(default=False)
    delivery_option = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(Product, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    