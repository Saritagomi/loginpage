# forms.py
from django import forms

class PasswordResetRequestForm(forms.Form):
    mobile_number = forms.CharField(max_length=15)

class PasswordResetVerifyForm(forms.Form):
    verification_code = forms.CharField(max_length=6)

class PasswordResetCompleteForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
