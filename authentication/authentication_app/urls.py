"""URL configuration for authenticationApp"""
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('verify-email/<uidb64>/<token>', views.verify_email, name='verify_email'),
    path('', views.home_view, name='home'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="authentication_app/password_reset_form.html"), name='password_reset'),
    path('password_reset/done', auth_views.PasswordResetDoneView.as_view(template_name="authentication_app/password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="authentication_app/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="authentication_app/password_reset_complete.html"), name='password_reset_complete'),
]
