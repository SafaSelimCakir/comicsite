# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from xsite.models import Profile,ProductImage
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate
from django import forms
from .models import Rating

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating', 'comment']



class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['product', 'image']


class CustomPasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Eski Şifre'}), label='Eski Şifre')
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Yeni Şifre'}), label='Yeni Şifre')
    new_password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Yeni Şifre (Tekrar)'}), label='Yeni Şifre (Tekrar)')

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        new_password_confirm = cleaned_data.get('new_password_confirm')

        if new_password != new_password_confirm:
            raise forms.ValidationError("Yeni şifreler eşleşmiyor.")
        return cleaned_data

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio']
        
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']




class UserProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['email'].initial = user.email
            self.fields['username'].initial = user.username

    username = forms.CharField(required=True)