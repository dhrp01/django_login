import logging

from django.core.cache import cache
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import LoginForm, SignupForm
from .models import UserProfile
from .utils import render_htmx_message

logger = logging.getLogger(__name__)

def login_view(request):
    """User login view for authentication project"""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            failed_attemps = cache.get(f'failed_login_{username}', 0)
            if failed_attemps > 5:
                context = {"message": "Account locked due to too many login attempts.", "status": "error"}
                return render_htmx_message(context)

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                send_mail(
                    "Verify email",
                    "Login attempt was made",
                    "your-email@gmail.com",
                    [user.email],
                    fail_silently=False
                )
                cache.delete(f'failed_login_{username}')
                logger.debug(f"Logged in as user {username}")
                success_response = JsonResponse({"message": "Login successful. Redirect..."})
                success_response['HX-Redirect'] = reverse('home')
                return success_response
            else:
                cache.set(f'failed_login_{username}', failed_attemps + 1, timeout=300)
                context = {"message": "Either the given username or password is invalid.", "status": "error"}
                return render_htmx_message(context)
        else:
            error_messages = [
                            f"{field}: {', '.join(errors)}"
                            for field, errors in form.errors.items()  # pyright: ignore
                        ]
            context = {"messages": error_messages, "status": "error"}
            return render_htmx_message(context)
    else:
        form = LoginForm()
    return render(request, 'authentication_app/login.html', {'form': form})

def signup_view(request):
    """New user signup view for authentication project"""
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            UserProfile.objects.create(user=user, phone=form.cleaned_data.get('phone'))  # pyright: ignore

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            email_verification_link = request.build_absolute_uri(f'/authentication_app/verify-email/{uid}/{token}')
            send_mail(
                "Verify email",
                f"Hi {user.username},\n\n Please verify your email address by clicking on the" \
                f"link below or copy pasting it in a browser:\n{email_verification_link}\n\nThank you, Authentication App",
                "your-email@gmail.com",
                [user.email],
                fail_silently=False
            )

            logger.debug(f"Created user {user.username} successfully")
            success_response = JsonResponse({"message": "Account Created. Check your mail for verification. Redirecting to login..."})
            success_response['HX-Redirect'] = reverse('login')
            return success_response
        else:
            error_messages = [
                            f"{field}: {', '.join(errors)}"
                            for field, errors in form.errors.items()  # pyright: ignore
                        ]
            context = {"messages": error_messages, "status": "error"}
            return render_htmx_message(context)
    else:
        form = SignupForm()

    return render(request, 'authentication_app/signup.html', {'form': form})

def verify_email(request, uidb64, token):
    """Handle email verification"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):  # pyright: ignore
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        logger.info(f"Email verified successful for user {user}")
        return redirect('login')
    else:
        logger.error("Invalid or experied link")
        context = {"message": "Invalid or experied link", "status": "error"}
        render_htmx_message(context)
        return redirect('signup')

def logout_view(request):
    """User logout view for authentication project"""
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    """Default home view after login is successful"""
    return render(request, 'authentication_app/home.html')
