from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Brand, Category, Product, Cart, CartItem
from user.models import User


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id","name","description","created_at"]
        

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    brand = BrandSerializer
    class Meta:
        model = Category
        fields = ["id","name","description","created_at","brand"]
        
        
class ProductSerializer(serializers.HyperlinkedModelSerializer):
    brand = CategorySerializer
    class Meta:
        model = Product
        fields = ["id","name","description","price","created_at","category"]

 
        
class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name','price']
        
        
class CartItemSerializer(serializers.ModelSerializer):

    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField(method_name='get_total_price')

    class Meta:
        model = CartItem
        fields = ['id','product','quantity','total_price']

    def get_total_price(self,cart_item:CartItem):
        return cart_item.quantity * cart_item.product.price
    
    
class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self,value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('محصول موجود نیست')
        return value
        
    def save(self, **kwargs):
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        cart_id = self.context['cart_id']
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id,product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id,**self.validated_data)

        return self.instance

    class Meta:
        model = CartItem
        fields = ['product_id','quantity']

class UpdateCartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ['quantity']
    
    
class CartSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True,read_only=True)
    total_price = serializers.SerializerMethodField(method_name='get_total_price')

    class Meta:
        model = Cart
        fields = ['id','items','total_price']

    def get_total_price(self,cart:Cart):
        return sum([ item.quantity * item.product.price for item in cart.items.all()])
    
    def save(self, **kwargs):
        user_id = self.context['user_id']
        user = get_object_or_404(User,pk=user_id)
        self.instance : Cart = Cart.objects.create(user=user,**self.validated_data)

        return self.instance
    

        
    