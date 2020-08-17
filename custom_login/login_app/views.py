from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm

# Create your views here.
def home(request):
	return render(request, 'home.html')

def signup(request):
	form = SignUpForm(request.POST)
	if form.is_valid():
		form.save()
		username = form.cleaned_data.get('username')
		password = form.cleaned_data.get('password1')
		user = authenticate(username=username, password=password)
		login(request, user)
		return redirect('home')
	return render(request, 'signup.html', {'form': form})

def logout_request(request):
	logout(request)
	return redirect('home')

def login_request(request):
	if request.method == 'POST':
		form = AuthenticationForm(request=request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				print("Invalid username or password")
		else:
			print("Invalid form")
	else:
		form = AuthenticationForm()
	return render(request, 'login.html', {'form': form})