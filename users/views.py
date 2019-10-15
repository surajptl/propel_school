from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm

# Create your views here.
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            full_name = form.cleaned_data.get('full_name')
            messages.success(request, f'Account created for {full_name}!')
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, "users/register.html", {'form' : form})
