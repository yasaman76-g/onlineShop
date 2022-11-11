from . import views
from django.urls import path
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register(r'brands', views.BrandViewSet)
router.register('categories', views.CategoryViewSet)
categories_router = routers.NestedSimpleRouter(router, r'brands', lookup='brand')
categories_router.register(r'categories', views.CategoryViewSet, basename='brand-categories')

urlpatterns = router.urls + categories_router.urls