import requests
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
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
from django.forms.utils import ErrorList
from django.http import Http404, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
## FUNCTION BASED
    
def get_upcoming_contests():
  """Gets the list of upcoming contests from the Codeforces API."""
  url = "https://codeforces.com/api/contest.list"
  headers = {
  "Authorization": "Bearer {}".format(settings.CODEFORCES_API_KEY)}
  try:
      response = requests.get(url, headers=headers)
      data = response.json()
      contests = []
      if "result" in data:
        for contest in data["result"]:
            if contest["phase"] == "BEFORE":
                now = datetime.datetime.now()
                contests.append(contest)
  except:
      contests = []   

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
        login(self.request , user,backend='django.contrib.auth.backends.ModelBackend')
        return view


class LoginView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/login.html'



def send_email(request):
    send_email_to_client()
    return redirect('/')


class CreateAssignment(LoginRequiredMixin,generic.CreateView):
    model = Assignment
    fields = ['title','question','submission_date','tags']
    template_name = 'cp_main/create_assignment.html'
    success_url = reverse_lazy('home')
    def form_valid(self, form):
        form.instance.user = self.request.user
        super(CreateAssignment, self).form_valid(form)
        return redirect('home')
    
    
class CreateQuestion(LoginRequiredMixin, generic.CreateView):
    model = Question
    fields = ['title','description','url']
    template_name = 'cp_main/create_question.html'
    success_url = reverse_lazy('create_assignment')
    def get_success_url(self, **kwargs):
        print(self.request)       
        if  kwargs != None:
            return reverse_lazy('create_assignment')
        else:
            return reverse_lazy('create_assignment')

class CreateNewQuestion(LoginRequiredMixin, generic.CreateView):
    model = Question
    fields = ['title','description','url']
    template_name = 'cp_main/create_new_question.html'
    success_url = reverse_lazy('view_questions')


def view_questions(request):
    questions = Question.objects.all()
    return render(request, 'cp_main/view_questions.html',{'questions':questions})

def view_assignments(request):
    assignments = Assignment.objects.all()
    return render(request, 'cp_main/view_assignments.html',{'assignments':assignments})

def view_assignment(request,slug):
    assignment = Assignment.objects.get(slug=slug)
    if request.method == 'POST':
        submit_form = SubmitForm(request.POST,request.FILES,instance=request.user)
        if submit_form.is_valid():
            submit_form_copy = submit_form.save(commit = False)
            submit_form_copy.user = request.user
            submit_form_copy.sub = assignment
            submit_form_copy.status = 'submitted'
            submit_form_copy.save()
            return redirect('view_assignments')
        else:
            return render(request, 'cp_main/view_assignment.html', {'assignment':assignment,'submit_form':submit_form,'submit_form_errors':submit_form.errors})
    else:
        submit_form = SubmitForm(instance=request.user)
        return render(request,'cp_main/view_assignment.html',{'submit_form':submit_form,'assignment':assignment})
    
class UpdateAssignment(LoginRequiredMixin, generic.UpdateView):
    model = Assignment
    fields = ['title','question','submission_date']
    template_name = 'cp_main/update_assignment.html'
    success_url = reverse_lazy('view_assignments')


class UpdateQuestion(LoginRequiredMixin, generic.UpdateView):
    model = Question
    fields = ['title','description','url']
    template_name = 'cp_main/update_question.html'
    success_url = reverse_lazy('view_questions')

def  delete_assignment(request, slug):
    assignment = Assignment.objects.get(slug=slug)
    if assignment:
        assignment.delete()
        return redirect('view_assignments')

def delete_question(request,fetched_slug):
    question = Question.objects.get(slug=fetched_slug)
    if question:
        question.delete()
        return redirect('view_questions')


