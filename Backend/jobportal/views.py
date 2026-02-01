from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from .models import *
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return render(request, 'software/contact.html', {'form': ContactForm(), 'success_message': 'Your message has been sent successfully!'})
    else:
        form = ContactForm()
    return render(request, 'software/contact.html', {'form': form})
def register(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_verification_email(request, user)
            return render(request, 'software/registration_complete.html')
    else:
        form = CustomUserForm()
    return render(request, 'software/register.html', {'form': form})

def send_verification_email(request, user):
    current_site = request.get_host()
    subject = 'Activate Your Account'
    activation_link = f'http://{current_site}/activate/{user.id}/'
    from_email = 'atigaddasusmitha789@gmail.com'
    to_email = user.email
    first_name = user.first_name
    last_name = user.last_name
    message = f'Dear {first_name} {last_name},\n' \
              f'Click the link to activate your account: {activation_link}'
    send_mail(subject, message, from_email, [to_email])

def activate_account(request, user_id):
    user = get_object_or_404(get_user_model(), id=user_id)
    user.is_active = True
    user.save()
    login(request, user)
    return HttpResponse(f"Your account is now activated. You can log in. \n\n" \
        f"Please Remember your username to login: {user.username}")

def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            pwd = request.POST.get('password')
            user = authenticate(request, username=name, password=pwd)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in Successfully")
                return redirect("/")
            else:
                messages.error(request, "Invalid User Name or Password")
                return redirect("/login")
        return render(request, "software/login.html")

def logout_page(request):
  if request.user.is_authenticated:
    logout(request)
    messages.success(request,"Logged out Successfully")
  return redirect("/")

class MyPasswordResetView(auth_views.PasswordResetView):
    template_name = 'software/password_reset_form.html'
    email_template_name = 'software/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

class MyPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'software/password_reset_done.html'

class MyPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'software/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class MyPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'software/password_reset_complete.html'

def home(request):
    softwarejobs=SoftwareJob.objects.all()
    if not request.user.is_authenticated:
        return render(request, "software/home.html", {'softwarejobs': softwarejobs})
    else:
        user_has_applied_jobs = JobSubmission.objects.filter(user=request.user, user_has_applied=True).values_list('SoftwareJob', flat=True)
        return render(request, "software/home.html", {'softwarejobs': softwarejobs, 'user_has_applied_jobs': user_has_applied_jobs})

def apply(request, job_id):
    job = get_object_or_404(SoftwareJob, pk=job_id)
    if request.method == 'POST':
        form = JobApplication(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user  # Set the user field here
            submission.SoftwareJob = job
            submission.user_has_applied = True
            submission.save()
            job.user_has_applied = True
            job.save()
            messages.success(request, 'Your Job Submission has been sent successfully!')
            return redirect('applied_jobs')
    else:
        form = JobApplication()
    return render(request, "software/apply.html", {'form': form, 'job': job})

def applied_jobs(request):
    user_applied_jobs = JobSubmission.objects.filter(user=request.user, user_has_applied=True)
    return render(request, "software/applied_jobs.html", {'user_applied_jobs': user_applied_jobs})

def about(request):
    return render(request, 'software/about.html')

def history(request):
    contact_submissions = ContactSubmission.objects.all()

    return render(request, 'software/history.html', {'ContactSubmissions': contact_submissions})
