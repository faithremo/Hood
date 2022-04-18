from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from django.db.models import fields
from .models import NeighbourHood, Post, Profile, Business

class CreateUserForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name','profile_picture','bio','email','neighbourhood','location']

class NeighbourHoodForm(forms.ModelForm):
    class Meta:
        model = NeighbourHood
        fields = ['name','location', 'picture', 'description', 'contact', 'health_department', 'police_authorities']

class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ['name', 'description', 'neighbourhood', 'email']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'post', 'hood']