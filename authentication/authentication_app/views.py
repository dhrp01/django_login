import logging

from django.core.cache import cache
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .validator import is_invalid_password, is_valid_email, is_valid_phone
from .utils import render_htmx_message

logger = logging.getLogger(__name__)

def login_view(request):
    """User login view for authentication project"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        failed_attemps = cache.get(f'failed_login_{username}', 0)
        if failed_attemps > 5:
            context = {"message": "Account locked due to too many login attempts.", "status": "error"}
            return render_htmx_message(context)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            cache.delete(f'failed_login_{username}')
            logger.debug(f"Logged in as user {username}")
            return redirect('home')
        else:
            cache.set(f'failed_login_{username}', failed_attemps + 1, timeout=300)
            context = {"message": "Either the given username or password is invalid.", "status": "error"}
            return render_htmx_message(context)

    return render(request, 'authentication_app/login.html')

def signup_view(request):
    """New user signup view for authentication project"""
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if not username or not firstname or not lastname or not email or not phone or not password or not confirm_password:
            context = {"message": "All fields are required.", "status": "error"}
            return render_htmx_message(context)

        if not is_valid_email(email):
            context = {"message": "Email is invalid.", "status": "error"}
            return render_htmx_message(context)

        if not is_valid_phone(phone):
            context = {"message": "Phone is invalid.", "status": "error"}
            return render_htmx_message(context)

        if User.objects.filter(username=username).exists():
            context = {"message": "Username already taken.", "status": "error"}
            return render_htmx_message(context)

        if User.objects.filter(email=email).exists():
            context = {"message": "Username already taken.", "status": "error"}
            return render_htmx_message(context)

        if password == confirm_password:
            invalid_messages = is_invalid_password(password)
            if not invalid_messages:
                try:
                    user = User.objects.create_user(
                        username=username,
                        firstname=firstname,
                        lastname=lastname,
                        email=email,
                        phone=phone,
                        password=password
                    )
                    user.save()
                    logger.debug(f"Created user {username} successfully")
                    return redirect('login')
                except Exception as e:
                    logger.error(f"Failed creating user {username}. Error: {e}")
                    context = {"message": f"Error creating account for user {username}.", "status": "error"}
                    return render_htmx_message(context)
            else:
                context = {"messages": messages, "status": "error"}
                return render_htmx_message(context)
        else:
            context = {"message": "Passwords do not match.", "status": "error"}
            return render_htmx_message(context)

    return render(request, 'authentication_app/signup.html')

def logout_view(request):
    """User logout view for authentication project"""
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    """Default home view after login is successful"""
    return render(request, 'authentication_app/home.html')
