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
from .models import *
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
        contests.append(contest)    
  return contests

@login_required
def home(request):
  contests = get_upcoming_contests()
  print(len(contests))
  a = {"contestes":contests}
  return render(request, 'cp_main/home.html', {"contests":contests})

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


def assignment_list(request):
    assignments = assignment.objects.all()
    context = {'assignments': assignments}
    return render(request, 'cp_main/assignment.html', context)

@login_required
def create_assignment(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        assignment = assignment.question(title=title, description=description)
        assignment.save()
        return redirect('assignment')
    else:
        return render(request, 'cp_main/create.html')
    
def view_submissions(request, assignment_id):
    assignment = assignment.objects.get(pk=assignment_id)
    submissions = submission.objects.filter(sub=assignment)
    context = {'assignment': assignment, 'submissions': submissions}
    return render(request, 'cp_main/view_submissions.html', context)

def download_file(request, assignment_id, submission_id):
    submission = submission.objects.get(pk=submission_id)
    file = submission.file
    response = HttpResponse(file, content_type='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename={}'.format(file.name)
    return response