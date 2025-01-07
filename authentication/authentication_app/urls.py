"""URL configuration for authenticationApp"""
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('verify-email/<uidb64>/<token>', views.verify_email, name='verify_email'),
    path('', views.home_view, name='home'),
]
