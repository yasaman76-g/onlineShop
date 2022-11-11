from rest_framework.viewsets import ModelViewSet
from .serializers import BrandSerializer, CategorySerializer
from .models import Brand, Category

# Create your views here.

class BrandViewSet(ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    
    
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.prefetch_related("brand_id").all()
    serializer_class = CategorySerializer
    def get_serializer_context(self):
        if self.kwargs.get("brand_pk"):
            context = {"brand_pk":self.kwargs["brand_pk"]}
            return context