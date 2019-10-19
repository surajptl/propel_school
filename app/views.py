from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from .forms import ApplicationForm
import json
from users.models import CustomUser
from app.models import Applicant

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


@login_required
def dashboard(request):
    print(Applicant.objects.values('approval').filter(applicant_id=1))
    if Applicant.objects.filter(applicant_id=request.user).count()==1:
       apply_message={'status':'You have submitted your application succesfully, please wait for further instructions'}
    #    app_status = Applicant.objects.
    else :apply_message={'status':'Apply for propel school to join the best prep school'}
    context={
        'apply_message':apply_message
    }
    return render(request, 'app/dashboard.html', context)
