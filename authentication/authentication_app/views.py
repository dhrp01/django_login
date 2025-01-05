import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

logger = logging.getLogger(__name__)

def login_view(request):
    """User login view for authentication project"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            logger.info(f"Logged in as user {username}")
            return redirect('home')
        else:
            logger.error(f"Either username or passsword is incorrect for user {username}")
            messages.error(request, 'Either the given username or password is invalid.')
    return render(request, 'authentication_app/login.html')

def signup_view(request):
    """New user signup view for authentication project"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            try:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                logger.info(f"Created user {username} successfully")
                messages.success(request, f'User {username} has been created successfull.')
                return redirect('login')
            except Exception as e:
                logger.error(f"Failed creating user {username}. Error: {e}")
                messages.error(request, f'Error creating account for user {username}.')
        else:
            logger.error("Passwords do no match")
            messages.error(request, 'Passwords do not match.')
    return render(request, 'authentication_app/signup.html')

def logout_view(request):
    """User logout view for authentication project"""
    logout(request)
    return redirect('login')

def home_view(request):
    """Default home view after login is successful"""
    return render(request, 'authentication_app/home.html')
