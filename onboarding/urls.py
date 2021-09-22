from django.urls import path
from . import views

urlpatterns = [
    path('get-otp/', views.OTPViews.get_otp, name='get-otp-api')
]
