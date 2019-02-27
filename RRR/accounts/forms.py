from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        email = User
        fields = {
            'username'
            'first_name'
            'last_name'
            'email'
            'password1'
            'password2'
        }
    
    def save(self, commit=True)
        user=super(RegistrationForm, self().save(comit=False)
        user.first_name = self