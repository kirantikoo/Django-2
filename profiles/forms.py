from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from profiles.models import Profile

class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    username = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']

class AvatarUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class CustomPasswordChangeForm(PasswordChangeForm):
    pass
