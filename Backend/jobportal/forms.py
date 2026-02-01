from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta


GENDER_CHOICES = [
    (None, 'Select Gender'),
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
]

class CustomUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter First Name'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter Last Name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Enter Email Address'}))
    phone_number = forms.CharField(max_length=10, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter Phone Number'}))
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=True, widget=forms.Select(attrs={}))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date','placeholder': 'dd-mm-yyyy'}))
    current_address = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter your Current Address'}))
    password1 = forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'placeholder': 'Enter Your Password'}))
    password2 = forms.CharField(label="Confirm Password",widget=forms.PasswordInput(attrs={'placeholder': 'Enter Confirm Password'}))

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'gender', 'date_of_birth', 'current_address', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("User with this Email already exists.")
        return email
    
    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')

        if date_of_birth:
            min_date_of_birth = datetime.now().date() - timedelta(days=365 * 18)
            if date_of_birth > timezone.now().date() or date_of_birth > min_date_of_birth:
                raise ValidationError("Please enter a valid Date of Birth atleast 18+ years old.")
        return date_of_birth

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        if not phone_number.isdigit() or not (6 <= int(phone_number[0]) <= 9) or len(phone_number) != 10:
            raise ValidationError("Please enter a valid phone number")

        return phone_number

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ['full_name', 'email', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Enter your Full Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your Email ID'}),
            'message': forms.Textarea(attrs={'placeholder': ' Enter your Message'}),
        }



class JobApplication(forms.ModelForm):
    class Meta:
        model = JobSubmission
        fields = ['full_name', 'education', 'branch', 'graduation_year', 'experience', 'resume']

        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
            'education': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your highest education'}),
            'branch': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your branch'}),
            'graduation_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your graduation year'}),
            'experience': forms.Select(attrs={'class': 'form-control'}),
            'resume': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf, .doc, .docx'}),
        }

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')

        # Add any custom validation for the resume file if needed

        return resume