from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm 
from django.http import HttpResponse 
from .forms import ApplicationForm

# Create your views here.

@login_required
def index(request):
    return render(request, 'app/index.html')


def application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        
        if form.is_valid():
        # name = form.cleaned_data['applicant_name']
        # print(name)
            print('here')
            form.save()
    form = ApplicationForm()
    return render(request, 'form.html', {'form':form})


