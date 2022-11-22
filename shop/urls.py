from . import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register(r'brands', views.BrandViewSet)
router.register('categories', views.CategoryViewSet)
router.register('products', views.ProductViewSet)
router.register('carts',views.CartViewSet,basename='carts')

categories_router = routers.NestedSimpleRouter(router, r'brands', lookup='brand')
categories_router.register(r'categories', views.CategoryViewSet, basename='brand-categories')

products_router = routers.NestedSimpleRouter(router, r'categories', lookup='category')
products_router.register(r'products', views.ProductViewSet, basename='category-products')

carts_router = routers.NestedSimpleRouter(router, r'carts', lookup='cart')
carts_router.register(r'items', views.CartItemViewSet, basename='cart-items')

urlpatterns = router.urls + categories_router.urls + products_router.urls + carts_router.urls