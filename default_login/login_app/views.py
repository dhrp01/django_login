from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


@login_required
def home(request):
	return render(request, 'default_login/home.html')


def signup(request):
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return render(request, 'default_login/home.html')
	return render(request, 'registration/sign_up.html', {'form' : UserCreationForm})
