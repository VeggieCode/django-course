from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField() #Atribute overrided

    class Meta:
        # The model we want to modify
        model = User
        # What fields are gonna be shown and in what order
        fields = ['username', 'email', 'password1', 'password2']