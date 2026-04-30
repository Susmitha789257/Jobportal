from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

from .forms import *
from .models import *


# =========================
# CONTACT
# =========================
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return render(request, 'software/contact.html', {'form': ContactForm()})
    else:
        form = ContactForm()
    return render(request, 'software/contact.html', {'form': form})


# =========================
# REGISTER + ACTIVATE
# =========================
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
    message = f'Dear {user.first_name} {user.last_name},\n\nClick to activate:\n{activation_link}'
    send_mail(subject, message, 'atigaddasusmitha789@gmail.com', [user.email])


def activate_account(request, user_id):
    user = get_object_or_404(get_user_model(), id=user_id)
    user.is_active = True
    user.save()
    login(request, user)
    return HttpResponse(
        f"Account activated successfully.\n\nUsername: {user.username}"
    )


# =========================
# LOGIN / LOGOUT
# =========================
def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        if user:
            login(request, user)
            messages.success(request, "Logged in Successfully")
            return redirect("/")
        messages.error(request, "Invalid username or password")
    return render(request, "software/login.html")


def logout_page(request):
    logout(request)
    messages.success(request, "Logged out Successfully")
    return redirect("/")


# =========================
# PASSWORD RESET
# =========================
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


# =========================
# HOME
# =========================
def home(request):
    softwarejobs = SoftwareJob.objects.all()
    if request.user.is_authenticated:
        user_has_applied_jobs = JobSubmission.objects.filter(
            user=request.user,
            user_has_applied=True
        ).values_list('SoftwareJob', flat=True)
        return render(request, "software/home.html", {
            'softwarejobs': softwarejobs,
            'user_has_applied_jobs': user_has_applied_jobs
        })
    return render(request, "software/home.html", {'softwarejobs': softwarejobs})


# =========================
# APPLY JOB
# =========================
@login_required
def apply(request, job_id):
    job = get_object_or_404(SoftwareJob, pk=job_id)
    if request.method == 'POST':
        form = JobApplication(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.SoftwareJob = job
            submission.user_has_applied = True
            submission.save()
            messages.success(request, 'Job applied successfully!')
            return redirect('applied_jobs')
    else:
        form = JobApplication()
    return render(request, "software/apply.html", {'form': form, 'job': job})


@login_required
def applied_jobs(request):
    jobs = JobSubmission.objects.filter(user=request.user, user_has_applied=True)
    return render(request, "software/applied_jobs.html", {'user_applied_jobs': jobs})


# =========================
# STATIC PAGES
# =========================
def about(request):
    return render(request, 'software/about.html')


def history(request):
    submissions = ContactSubmission.objects.all()
    return render(request, 'software/history.html', {'ContactSubmissions': submissions})


# =========================
# 🔥 BACKEND API (IMPORTANT)
# =========================
def api_jobs(request):
    jobs = SoftwareJob.objects.all()
    data = []

    for job in jobs:
        data.append({
            "id": job.id,
            "job_name": job.job_name,
            "skills": job.skills,
            "min_experience": job.min_experience,
            "max_experience": job.max_experience,
            "education": job.education,
            "min_package": job.min_package,
            "max_package": job.max_package,
            "work_mode": job.work_mode,
            "openings": job.openings,
            "description": job.job_description,
        })

    return JsonResponse({"jobs": data}, status=200)
