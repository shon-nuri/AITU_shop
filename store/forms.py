from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Review

class SignupForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['username','email', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),  # Dropdown for rating (1-5)
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your review here...'})
        }