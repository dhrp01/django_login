from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

GENDER_CHOICE = (('-', '-'), ('M', 'Male'), ('F', 'Female'))


class SignUpForm(UserCreationForm):
	username = forms.EmailField(max_length=200, help_text="Enter valid email id. Less than 200")
	firstname = forms.CharField(max_length=200, help_text="Enter first name")
	lastname = forms.CharField(max_length=200, help_text="Enter last name")
	gender = forms.ChoiceField(choices=GENDER_CHOICE, required=False)

	class Meta:
		model = User
		fields = ('username', 'firstname', 'lastname', 'gender',)