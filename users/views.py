from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .token import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_text
from django.http import HttpResponse
from .models import CustomUser
from django.contrib.auth import login
# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

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

# def register(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False
#             user.save()
#             current_site = get_current_site(request)
#             subject = 'Activate your blog account.'
#             message = render_to_string('acc_active_email.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid':urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token':account_activation_token.make_token(user),
#             })
#             to = form.cleaned_data.get('email')
#             email_by_admin(subject, message, to)
#             return HttpResponse('Please confirm your email address to complete the registration')
#     else:
#         form = CustomUserCreationForm()
#         return render(request, "users/register.html", {'form' : form})


def email_by_admin(subject, text_content, to):
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, text_content, from_email, [to])
    return None

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')