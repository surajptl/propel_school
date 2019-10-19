from django.shortcuts import render, redirect
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
            instance = form.save(commit=False)
            instance.applicant_id = CustomUser.objects.get(id=request.user.id)
            instance.save()
            print(request.user.email)
        return redirect('dashboard')
    form = ApplicationForm()
    return render(request, 'app/form.html', {'form':form})


@login_required
def dashboard(request):
    if Applicant.objects.filter(applicant_id=request.user).count()==1:
       apply_message = {'status':'You have submitted your application succesfully, please wait for further instructions'}
    #    app_status = Applicant.objects.
    else :apply_message={'status':'Apply for propel school to join the best prep school'}
    profile_messages = dashboard_user_profile_builder(request)
    print(profile_messages)
    context={
        'apply_message':apply_message,
        'profile_messages':profile_messages
    }
    dashboard_user_profile_builder(request)
    return render(request, 'app/dashboard.html', context)


def dashboard_user_profile_builder(request):
    print(Applicant.objects.values('approval').get(applicant_id=request.user)['approval'])
    profile_messages = {
        'app_status' : Applicant.objects.values('approval').get(applicant_id=request.user)['approval'],
        'last_login' : str(request.user.last_login),
        'fcc_link'   : Applicant.objects.values('fcc_link').get(applicant_id=request.user)['fcc_link'],
        'd_o_b'      : str(Applicant.objects.values('d_o_b').get(applicant_id=request.user)['d_o_b'])
    }
    print(request.user.last_login)
    return profile_messages
