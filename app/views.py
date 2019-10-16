from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm 
from django.http import HttpResponse 
from .forms import ApplicationForm, SnippetForm
# Create your views here.

def application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['applicant_name']
            form.save()
            print(name)


    form = ApplicationForm
    return render(request, 'form.html', {'form':form})


def snippet_detail(request):    
    form = SnippetForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            print("views/snippet")
            form.save()
    
    return render(request, 'form.html', {'form':form})
