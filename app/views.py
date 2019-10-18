from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from .forms import ApplicationForm
from users.models import CustomUser

# Create your views here.
def index(request):
    return render(request, 'app/index.html')

@login_required
def application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            instance              = form.save(commit=False)
            instance.applicant_id = CustomUser.objects.get(id=request.user.id)
            instance.save()
            print(request.user.email)
    form = ApplicationForm()
    return render(request, 'app/form.html', {'form':form})
