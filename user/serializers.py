from django.core.validators import MinLengthValidator, MaxLengthValidator
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name','mobile','email','password']
        extra_kwargs = {'password': {'write_only': True,'required':False}}
        
    mobile = serializers.CharField(
        validators=[
            MinLengthValidator(
                11,message='لطفا تلفن همراه خود را به درستی وارد کنید.'),
            MaxLengthValidator(
                11,message='لطفا تلفن همراه خود را به درستی وارد کنید.')
        ]
    )
    
          
    def create(self, validated_data):
        password = self.context["code"]
        user = User(mobile=validated_data.get("mobile"),username=validated_data.get("mobile"))
        user.set_password(password)
        user.save()
        return user
    
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name','email','password']
        extra_kwargs = {'password': {'write_only': True,'required':False}}
        
    def update(self, instance:User, validated_data):
        super().update(instance, validated_data)
        instance.set_password(validated_data.get("password"))
        instance.save()
        return instance