from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
from .models import Brand, Category


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id","name","description","created_at"]
        

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    brand = BrandSerializer
    class Meta:
        model = Category
        fields = ["id","name","description","created_at","brand"]
        
    def create(self, validated_data):
        if self.context:
            brand_pk = self.context.get("brand_pk")
            brand = Brand.objects.get(pk=brand_pk)
            return Category.objects.create(brand=brand,**validated_data)
        return Category.objects.create(**validated_data)
        
    