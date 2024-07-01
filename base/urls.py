
from django.urls import path,include
from django.contrib.auth import views 
from . import views

urlpatterns = [
    path("", views.home, name ="home"),
    # path("signup/", authView , name= "authView"),
    path("login/", views.loginView , name= "login"),
#for reset password
    path("accounts/", include("django.contrib.auth.urls")),
    #path('password_reset/', views.password_reset_request, name='password_reset_request'),
    path('password_reset_request/', views.password_reset_request, name='password_reset_request'),
    path('password_reset/verify/', views.password_reset_verify, name='password_reset_verify'),
    path('password_reset/complete/', views.password_reset_complete, name='password_reset_complete'),

]

   
