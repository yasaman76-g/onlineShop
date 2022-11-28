#https://github.com/akjasim/cb_dj_custom_user_model/
#https://www.youtube.com/watch?v=SbU2wdPIcaY

from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.contrib.auth.models import AbstractUser,BaseUserManager

class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, mobile, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not mobile:
            raise ValueError('تلفن همراه خودرا وارد کنید')
        email = self.normalize_email(email)
        user = self.model(mobile=mobile, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, mobile, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(mobile, email, password, **extra_fields)

    def create_superuser(self, mobile, email=None, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(mobile, email, password, **extra_fields)


class User(AbstractUser):
    username = None
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
    
    avatar = models.ImageField(upload_to="images/user",blank=True,null=True)
    
    USERNAME_FIELD = "mobile"
    REQUIRED_FIELDS = []

    
    objects = CustomUserManager()
    
    def __str__(self):
        if self.last_name is not None:
            return f"{self.first_name} - {self.last_name}"
        return self.mobile

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
        