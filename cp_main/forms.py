from django import forms 
from .models import *
from django.contrib.auth.models import User
from tinymce.widgets import TinyMCE

class UserForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name']
class ProfileForm(forms.ModelForm):
    codeforces_username = forms.CharField(max_length=100,required=True)
    leetcode_username = forms.CharField(max_length=100,required=True)
    codechef_username = forms.CharField(max_length=100,required=True)
    admitted_year = models.CharField(max_length = 500,blank=True)
    registration_no = models.CharField(max_length=10,blank=True)
    class Meta:
        model = Profile
        fields = ['Bio','codeforces_username','leetcode_username','codechef_username','registration_no','admitted_year']


