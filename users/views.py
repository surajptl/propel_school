from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect('login')
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            full_name = form.cleaned_data.get('full_name')
            messages.success(request, 'Hi {}, your Account created successfully'.format( full_name ))
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, "users/register.html", {'form' : form})
