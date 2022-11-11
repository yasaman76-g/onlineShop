from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    mobile = models.CharField(
        max_length=11,
        unique=True,
        validators=[
            MinLengthValidator(
                11,message='لطفا تلفن همراه خود را به درستی وارد کنید.'),
            MaxLengthValidator(
                11,message='لطفا تلفن همراه خود را به درستی وارد کنید.')
        ]
    )

class UserVerifyCode(models.Model):
    mobile = models.CharField(max_length=11)
    code = models.CharField(max_length=6)
    ip = models.GenericIPAddressField(protocol='both')
    expire_at = models.DateTimeField()
    
    class Meta:
        db_table = 'user_verify_code'
        
        
class UserLogLogin(models.Model):
    mobile = models.CharField(max_length=11)
    ip = models.GenericIPAddressField(protocol='both')
    logged_in = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'user_log_login'
        