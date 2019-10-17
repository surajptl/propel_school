from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from .forms import ApplicationForm

# Create your views here.
def index(request):
    return render(request, 'app/index.html')

@login_required
def application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save()
    form = ApplicationForm()
    return render(request, 'app/form.html', {'form':form})
