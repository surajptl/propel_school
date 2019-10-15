from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm 
from django.http import HttpResponse 
from .forms import ApplicationForm
# Create your views here.

def application(request):
    form = ApplicationForm
    return render(request, 'form.html', {'form':form})