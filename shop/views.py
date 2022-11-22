from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import ListModelMixin,CreateModelMixin,RetrieveModelMixin,DestroyModelMixin
from .serializers import BrandSerializer, CategorySerializer, ProductSerializer, CartSerializer,CartItemSerializer,AddCartItemSerializer,UpdateCartItemSerializer
from .models import Brand, Category, Product, Cart, CartItem

# Create your views here.

class BrandViewSet(ListModelMixin,RetrieveModelMixin,GenericViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    
    
class CategoryViewSet(ListModelMixin,RetrieveModelMixin,GenericViewSet):
    queryset = Category.objects.prefetch_related("brand").all()
    serializer_class = CategorySerializer
    
class ProductViewSet(ListModelMixin,RetrieveModelMixin,GenericViewSet):
    queryset = Product.objects.prefetch_related("category").all()
    serializer_class = ProductSerializer
    
class CartViewSet(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(id=self.kwargs['pk']).prefetch_related('items__product')
    
    def get_serializer_context(self):
        return {'user_id':self.request.user.id}
    
class CartItemViewSet(ModelViewSet):
    http_method_names = ['get','post','patch','delete']
    
    def get_queryset(self):
        return CartItem.objects \
            .filter(cart_id=self.kwargs['cart_pk']) \
            .select_related('product')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id':self.kwargs['cart_pk']}

    