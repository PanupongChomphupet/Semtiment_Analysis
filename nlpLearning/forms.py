from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegisterForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=[('teacher', 'Teacher'), ('student', 'Student')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'})
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'})
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'})
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password1', 'password2']

class CommentForm(forms.Form):
    subject = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))