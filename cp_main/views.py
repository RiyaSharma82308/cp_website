from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm 
# Create your views here.
def home(request):
    return render(request,'cp_main/home.html')

class Signup(generic.CreateView):