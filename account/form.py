from django import forms
from django.contrib.auth.models import User
from account.models import CreatorProfile, Profile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')


class CreatorProfileForm(forms.ModelForm):
    class Meta:
        model = CreatorProfile
        fields = ('channel_name', 'phonenumber', 'bio',
                  'acct_name', 'acct_number', 'bank_name')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image',)
