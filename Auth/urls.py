# Parents/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import Login_Parents,VerifyOtpAPI,Login_User

urlpatterns =[
    path('verify_otp', VerifyOtpAPI.as_view()),  # sử dụng router thay vì DefaultRouter
    path('login_user', Login_User.as_view()),  # sử dụng router thay vì DefaultRouter
]