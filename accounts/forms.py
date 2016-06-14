from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import ActivateKey, UserProfile


class VerifyForm(forms.ModelForm):
    class Meta:
        model = ActivateKey
        fields = ('key',)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('pic', 'about_me')


class UserForm(UserCreationForm):
    email = forms.EmailField(required=True)

