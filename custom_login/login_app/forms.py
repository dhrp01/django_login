from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
	# username = forms.CharField(max_length=30)
	username = forms.EmailField(max_length=200, help_text="Enter valid email id. Less than 200")

	class Meta:
		model = User
		fields = ('username',)