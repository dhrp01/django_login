from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .validator import is_valid_email, is_valid_phone, is_invalid_password

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

class SignupForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'confirm_password'}), required=True)
    phone = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'id': 'phone'}), required=True, label="Phone Number")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'id': 'username'}),
            'email': forms.EmailInput(attrs={'id': 'email'}),
            'password': forms.PasswordInput(attrs={'id': 'password'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not is_valid_email(email):  # pyright: ignore
            raise ValidationError("Invalid email address.")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already taken.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        invalid_messages = is_invalid_password(password)  # pyright: ignore
        if invalid_messages:
            raise ValidationError(invalid_messages)
        return password

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError("Passwords do not match.")
        return confirm_password

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get('phone')
        if not is_valid_phone(phone):  # pyright: ignore
            self.add_error('phone', "Invalid phone number.")
        return cleaned_data
