import requests
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from .forms import *
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm 
from django.utils.timezone import make_aware 
import datetime 
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from requests import get
import pandas as pd
from django.conf import settings
from django.urls import reverse
from .models import User
from django.test.client import Client
from django.contrib.auth.decorators import login_required,user_passes_test
from .utils import  send_email_to_client

## FUNCTION BASED
    
def get_upcoming_contests():
  """Gets the list of upcoming contests from the Codeforces API."""

  url = "https://codeforces.com/api/contest.list"
  headers = {
    "Authorization": "Bearer {}".format(settings.CODEFORCES_API_KEY)
  }

  response = requests.get(url, headers=headers)
  data = response.json()
  contests = []
  if "result" in data:
    for contest in data["result"]:
      if contest["phase"] == "BEFORE":
        now = datetime.datetime.now()
        if datetime.datetime.fromtimestamp(contest["startTimeSeconds"]) == now :
            contests.append(contest)

  return contests

@login_required
def home(request):
  """Renders the home page of the web application."""
  contests = get_upcoming_contests()
  return render(request, 'cp_main/home.html', {"contestes":contests})

def all_users(request):
   all_profiles = Profile.objects.all()
   return render(request, 'cp_main/all_user_profiles.html', {"all_profiles":all_profiles} )


@login_required
def profile(request,slug):
    if request.method == 'POST':
        user_form = UserForm(request.POST,instance = request.user)
        profile_form = ProfileForm(request.POST,request.FILES,instance = request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            profile_form_copy = profile_form.save(commit = False)
            user_form.save()
            profile_form_copy.save()
          # messages.success(request,'Profile Updated Successfully')
            return redirect('home')
        else:
            return render(request, 'cp_main/profile.html', {'user_form':user_form,'profile_form':profile_form,'user_form_errors':user_form.errors,'profile_form_errors':profile_form.errors})
    else:
        user_form = UserForm(instance = request.user)
        profile_form = ProfileForm(instance = request.user.profile)
        return render(request,'cp_main/profile.html',{'user_form':user_form,'profile_form':profile_form})


##  Class Based
class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        view = super(SignUp, self).form_valid(form)
        username, password = form.cleaned_data.get('username'),form.cleaned_data.get('password')
        user =  authenticate(username=username , password=password)
        user = form.save()
        login(self.request , user)
        return view


class LoginView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/login.html'



def send_email(request):
    send_email_to_client()
    return redirect('/')