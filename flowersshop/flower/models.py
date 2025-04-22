# Create your models here.


from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.CharField(max_length=255)
    average_rating = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()

class Cart(models.Model):
    user_id = models.BigIntegerField()  # Assuming user_id is an integer
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.IntegerField()

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Review(models.Model):
    user_id = models.BigIntegerField()
    text = models.TextField()
    rating = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)