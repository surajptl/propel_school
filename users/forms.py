from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ['email','full_name',]


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ['email','full_name',]

