from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class UserForm(UserCreationForm):
    """Class formulaire utilisateur"""
    class Meta:  # Utilisez "Meta" avec une majuscule
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']
       
       

class ProfileForm(forms.ModelForm):
    class Meta:  # Utilisez "Meta" avec une majuscule
        model = Profile
        fields = ['bio', 'photo', 'type_profile']
     
