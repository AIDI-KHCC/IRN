# users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Document

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['institution', 'mobile', 'khcc_employee_number', 'title', 'role', 'photo', 'cv']

class LoginForm(forms.Form):
    username_or_email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['document_type', 'other_document_name', 'issue_date', 'expiry_date', 'file']
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        document_type = cleaned_data.get('document_type')
        other_document_name = cleaned_data.get('other_document_name')

        if document_type == 'Other' and not other_document_name:
            raise forms.ValidationError("Please specify the document name.")

        return cleaned_data
