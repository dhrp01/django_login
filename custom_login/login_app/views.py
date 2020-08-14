from django.shortcuts import render
from django.contrib.auth import login, authenticate
from .forms import SignUpForm

# Create your views here.
def home(request):
	return render(request, 'home.html')

def signup(request):
	form = SignUpForm(request.POST)
	if form.is_valid():
		form.save()
		username = form.cleaned_data.get('username')
		password = form.cleaned_data.get('password')
		user = authenticate(username=username, password=password)
		login(request, user)
		return redirect('home')
	return render(request, 'signup.html', {'form': form})