from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from .forms import ApplicationForm, JoiningConfirmationForm, EditApplicationForm
import json
from users.models import CustomUser
from app.models import Applicant
from django.forms.models import model_to_dict


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
        return redirect('dashboard')
    form = ApplicationForm()
    return render(request, 'app/form.html', {'form':form})


@login_required
def edit_application(request):
    print(Applicant.objects.values('join_confirm').filter(applicant_id=request.user))
    if request.method == 'POST':
        form = EditApplicationForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.applicant_id = CustomUser.objects.get(id=request.user.id)
            instance.save()
        return redirect('dashboard')
    else:
       applicant = Applicant.objects.get(applicant_id=request.user)
       form = EditApplicationForm(initial=model_to_dict(applicant))
    return render(request, 'app/edit_application.html', {'form':form})


@login_required
def dashboard(request):
    
    if request.method == 'POST':
        form = JoiningConfirmationForm(request.POST or None)
        #print(form['join_confirm'])
        #print((request.POST['join_confirm']))
        #print(Applicant.objects.get(applicant_id=request.user))
        if form.is_valid():
            instance = Applicant.objects.get(applicant_id=request.user)
            instance.join_confirm = request.POST['join_confirm']
            instance.attended_propel_before = request.POST['attended_propel_before']
            instance.save()
        return redirect('dashboard')
    form = JoiningConfirmationForm()

    if Applicant.objects.filter(applicant_id=request.user).count()==1:
        apply_message = {'status':'You have submitted your application succesfully, please wait for further instructions'}
    else :
        apply_message={'status':'Apply for propel school to join the best prep school'}

    # Bug corrected: new login users unable to access dashboard
    if Applicant.objects.values('applicant_id').filter(applicant_id=request.user).exists():
        profile_messages = dashboard_user_profile_builder(request)
        context={
        'apply_message':apply_message,
        'profile_messages':profile_messages
        }
        return render(request, 'app/dashboard.html', context)

    else: 
        profile_messages = {
            'application' : False
        }
        context={
        'apply_message':apply_message,
        'profile_messages':profile_messages
        }
        return render(request, 'app/dashboard.html', context)

    

def dashboard_user_profile_builder(request):
    
    profile_messages = {
        'application' : Applicant.objects.values('applicant_id').filter(applicant_id=request.user).count(),
        'app_status_code' : int(Applicant.objects.values('approval').get(applicant_id=request.user)['approval']),
        'app_status' : dashboard_profile_status_builder(int(Applicant.objects.values('approval').get(applicant_id=request.user)['approval'])),
        'last_login' : str(request.user.last_login),
        'fcc_link'   : Applicant.objects.values('fcc_link').get(applicant_id=request.user)['fcc_link'],
        'd_o_b'      : str(Applicant.objects.values('d_o_b').get(applicant_id=request.user)['d_o_b']),
        'phone_number'   : Applicant.objects.values('phone_number').get(applicant_id=request.user)['phone_number'],
        'join_form' : Applicant.objects.values('join_confirm').get(applicant_id=request.user)['join_confirm']
    }
    return profile_messages


def dashboard_profile_status_builder(status_code):
    switcher = {
        1: "Eligible, await further instructions",
        2: "Please make your FreeCodeCamp profile as public",
        3: "Please get 100+ points on FreeCodeCamp to get eligible",
        4: "Please provide correct FreeCodeCamp profile link",
        5: "Shortlisted, Please confirm your joining in the form below",
        6: "Joined Propel",
        7: "Propel challenge received",
        8: "Given extended propel challenge"
    }
    return switcher.get(status_code)
