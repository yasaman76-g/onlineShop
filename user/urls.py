from . import views
from django.urls import path

urlpatterns = [
    path("get_user/",views.GetUser.as_view(),name="get-user"),
    path("register/",views.Register.as_view(),name="register"),
    path("update_profile/",views.UpdateUserProfile.as_view(),name="update-profile"),
    path("login/",views.LoginUser.as_view(),name="login"),
]