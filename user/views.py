from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from helper.email import send_email_template
from .models import User, UserLogLogin,UserVerifyCode
from .serializers import UserSerializer,UpdateUserSerializer
from random import randrange
from datetime import datetime, timedelta
import requests
import json

class GetUser(APIView):
    def get(self,request:HttpRequest):
        mobile = request.GET.get("mobile")
        user:User = User.objects.filter(mobile=mobile).first()
        is_new_user = True
        if user is not None:
            if not user.is_active:
                raise AuthenticationFailed("کاربر مورد نظر فعال نیست.")
            else:
                is_new_user = False
                data = {
                "is_new_user" : is_new_user,
                "mobile" : mobile,
                "message" : "رمز عبور خود را وارد کنید."
                }
                return Response(data=data,status=status.HTTP_200_OK)
        else:
            verification_code = randrange(100000,1000000)
            print(verification_code)
            expire_at = datetime.now() + timedelta(minutes = 5)
            ip = request.META['REMOTE_ADDR']
            UserVerifyCode.objects.create(mobile=mobile,code=verification_code,ip=ip,expire_at=expire_at)
            data = {
               "is_new_user" : is_new_user,
               "message" : f"لطفا کد ارسالی به {mobile} وارد نمایید."
            }
            return Response(data=data,status=status.HTTP_200_OK)
        
        
class Register(APIView):
    def post(self,request:HttpRequest):
        mobile = request.POST.get("mobile")
        code = request.POST.get("code")
        
        #Check user is not block
        ip = request.META['REMOTE_ADDR']
        key_ip = f"banned-ip-{ip}"
        key_mobile = f"banned-mobile-{mobile}"
        if cache.get(key_ip) is not None or cache.get(key_mobile) is not None:
            data = {
               "message" : "این شماره تلفن جزو بلک لیست می باشد."
            }
            return Response(data=data,status=status.HTTP_403_FORBIDDEN) 
        
        check_code = UserVerifyCode.objects.filter(mobile=mobile,code=code,expire_at__gt=datetime.now()).first()
        if check_code is not None:
            serializer = UserSerializer(
                data=request.data, context={"code": code})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            send_email_template(template_name="emails/register_user.html",context={"mobile" : mobile},to=['y.golesorkh@gamil.com'])

            UserVerifyCode.objects.filter(
                mobile=mobile, code=code).update(expire_at=datetime.now())
            
            url = "http://"+ request.get_host() +"/api/token/"
            headers = {
                "Content-Type" : "application/json",
            }
            
            data = {
                "mobile": mobile, 
                "password": code
            }
            
            response = requests.post(url, data=json.dumps(data),headers=headers)
            return Response(response.json())
            
        
        #Check the number of attempts to get code
        count_of_code = UserVerifyCode.objects.filter(
            mobile=mobile, expire_at__gt=datetime.now(),ip=ip).count()
        if count_of_code >= 3:
            cache.set(key_ip,mobile,60*60)
            cache.set(key_mobile,mobile,60*60)
            data = {
               "message" : "ای پی شما به مدت یک ساعت بلاک می باشد"
            }
            return Response(data,status=status.HTTP_403_FORBIDDEN)
        
        #Check the number of wrong code
        if "count_code" in request.session:
            count_wrong_code = request.session["count_code"] + 1
        else:
            count_wrong_code = 1
            
        request.session["count_code"] = count_wrong_code
            
        if count_wrong_code >= 3:
            cache.set(key_ip,mobile,60*60)
            cache.set(key_mobile,mobile,60*60)
            del request.session["count_code"]
            data = {
               "message" : "ای پی شما به مدت یک ساعت بلاک شد."
            }
            return Response(data,status=status.HTTP_403_FORBIDDEN)
        
        
        data = {
               "message" : "کد وارد شده صحیح نمیباشد"
        }
        return Response(data)
           
            
class UpdateUserProfile(APIView):
    def patch(self,request:HttpRequest):
        user = get_object_or_404(User,pk=request.user.id)
        serializer = UpdateUserSerializer(user,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)



class LoginUser(APIView):
    def post(self,request:HttpRequest):
        mobile = request.POST.get("mobile")
        password = request.POST.get("password")  
        
        #Check user is not block
        ip = request.META['REMOTE_ADDR']
        key_ip = f"banned-ip-{ip}"
        key_mobile = f"banned-mobile-{mobile}"
        if cache.get(key_ip) is not None or cache.get(key_mobile) is not None:
            data = {
               "message" : "این شماره تلفن جزو بلک لیست می باشد."
            }
            return Response(data=data,status=status.HTTP_403_FORBIDDEN) 
        
        user:User = User.objects.filter(mobile=mobile).first()
        if user is not None:
            if user.check_password(password):
                UserLogLogin.objects.create(mobile=mobile,ip=ip,logged_in=1)
                
                serializer = UserSerializer(user)
                url = "http://"+ request.get_host() +"/api/token/"
                headers = {
                    "Content-Type" : "application/json",
                }
                
                data = {
                    "mobile": mobile, 
                    "password": password
                }
                
                response = requests.post(url, data=json.dumps(data),headers=headers)
                
                return Response(response.json())
            else:
                UserLogLogin.objects.create(mobile=mobile,ip=ip,logged_in=0)
                
                #Check the number of wrong password
                if "count_password" in request.session:
                    count_wrong_password = request.session["count_password"] + 1
                else:
                    count_wrong_password = 1
                    
                request.session["count_password"] = count_wrong_password
                    
                if count_wrong_password >= 3:
                    cache.set(key_ip,mobile,60*60)
                    cache.set(key_mobile,mobile,60*60)
                    del request.session["count_password"]
                    data = {
                    "message" : "ای پی شما به مدت یک ساعت بلاک شد."
                    }
                    return Response(data,status=status.HTTP_403_FORBIDDEN)
        
                #Check number to attemps login with same ip
                failed_login_count = UserLogLogin.objects.filter(
                    ip=ip, logged_in=0, created_at__gt=(datetime.now() - timedelta(minutes=5))).count()
                if failed_login_count >= 3:
                    cache.set(key_ip,mobile,60*60)
                    cache.set(key_mobile,mobile,60*60)
                    data = {
                        "message" : "ای پی شما به مدت یک ساعت بلاک شد."
                    }
                    return Response(data,status=status.HTTP_403_FORBIDDEN)
                
                raise AuthenticationFailed('رمز عبور خود را به درستی وارد کنید')
        else:
            raise AuthenticationFailed("کاربر مورد نظر یافت نشد.")