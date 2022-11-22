from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from uuid import uuid4

# Create your models here.

class Brand(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.name
    

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE,related_name='categories')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(1)])
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.name
    

class Cart(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid4)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )

    class Meta:
        unique_together = [['cart','product']]
