from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=20, null=True)
    profile_pic = models.ImageField(default="default.svg", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(this):
        return f"{this.name}"

class Tag(models.Model):
    tag = models.CharField(max_length=200, null=True)

    def __str__(this):
        return f"{this.tag}"
        

class Product(models.Model):
    CATEGORY = (
        ('Indoor', 'Indoor'),
        ('Out door', 'Outdoor')
    )
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    description = models.CharField(max_length=300, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(this):
        return f"{this.name}"

class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered')
    )

    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=16, choices=STATUS)
    note= models.CharField(max_length=1000, null=True)
    def __str__(this):
        return f"{this.product.name}"   
