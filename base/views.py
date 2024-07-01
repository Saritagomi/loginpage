from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from django.conf import settings
# views.py
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from twilio.rest import Client
from .forms import PasswordResetRequestForm, PasswordResetVerifyForm, PasswordResetCompleteForm

def send_verification_code(mobile_number, code):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f"Your verification code is {code}",
        from_=settings.TWILIO_PHONE_NUMBER,
        to=mobile_number
    )

def password_reset_request(request):
    print('hello')
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            mobile_number = form.cleaned_data['mobile_number']
            user = User.objects.filter(profile__mobile_number=mobile_number).first()  # Assuming a Profile model with a mobile_number field
            if user:
                verification_code = '123456'  # Generate a random code in production
                send_verification_code(mobile_number, verification_code)
                request.session['mobile_number'] = mobile_number
                request.session['verification_code'] = verification_code
                return redirect('password_reset_verify')
    else:
        form = PasswordResetRequestForm()
    return render(request, 'password_reset_request.html', {'form': form})

def password_reset_verify(request):
    if request.method == 'POST':
        form = PasswordResetVerifyForm(request.POST)
        if form.is_valid():
            entered_code = form.cleaned_data['verification_code']
            stored_code = request.session.get('verification_code')
            if entered_code == stored_code:
                return redirect('password_reset_complete')
    else:
        form = PasswordResetVerifyForm()
    return render(request, 'password_reset_verify.html', {'form': form})

def password_reset_complete(request):
    if request.method == 'POST':
        form = PasswordResetCompleteForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']
            if new_password == confirm_password:
                mobile_number = request.session.get('mobile_number')
                user = User.objects.filter(profile__mobile_number=mobile_number).first()
                if user:
                    user.password = make_password(new_password)
                    user.save()
                    return redirect('password_reset_complete_done')
    else:
        form = PasswordResetCompleteForm()
    return render(request, 'password_reset_complete.html', {'form': form})

def password_reset_complete_done(request):
    return render(request, 'password_reset_complete_done.html')



@login_required

def home(request):
    return render(request ,"home.html", {} )

def loginView(request):

    #login -> username password -> User ->login ->login 

    print('login started')
    if request.method == "POST":
        form = UserCreationForm(request.POST or None)
        print(form)
        if form.is_valid():
            form.save()
            return HttpResponse("Login Sucessfully")
    else:
        form = UserCreationForm()
    return render(request, "registration/login.html", {"form": form})

# Create your views here.
