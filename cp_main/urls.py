"""miccp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin,auth
from django.urls import path,include
from .import views


urlpatterns = [
    path('profile/<slug:slug>', views.profile, name='profile'),
    path('all_users', views.all_users, name ='all_users'),
    path('send/email/', views.send_email ,  name="send_email"),

    #Assignments
    path('create/assignment', views.CreateAssignment.as_view() , name="create_assignment"),
    path('update/assignment/<slug:slug>', views.UpdateAssignment.as_view(), name="update_assignment"),
    path('delete/assignment/<slug:slug>', views.delete_assignment, name="delete_assignment"),
    path('view/assignments', views.view_assignments, name="view_assignments"),
    path('view/assignment/<slug:slug>', views.view_assignment, name="view_assignment"),
    
    #Questions
    path('create/question', views.CreateQuestion.as_view() , name="create_question"),
    path('view/questions', views.view_questions, name="view_questions"),
    path('update/question/<slug:slug>', views.UpdateQuestion.as_view(), name="update_question"),
    path('delete/question/<slug:fetched_slug>', views.delete_question, name="delete_question"),
    path('create/new/question', views.CreateNewQuestion.as_view(), name="create_new_question"),
    
]
