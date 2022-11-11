from django.db import models

# Create your models here.

class Brand(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE,related_name='categories')
    created_at = models.DateTimeField(auto_now_add=True)