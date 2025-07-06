from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth import get_user_model
from django.utils import timezone

class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    username = models.CharField(max_length=150, unique=True, default='sdeuser789')
    phone_number = models.CharField(null=True, blank=True,max_length=10, verbose_name='Phone number')
    gender = models.CharField(null=True, blank=True,max_length=10, choices=GENDER_CHOICES, verbose_name='Gender')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='Date of birth')
    current_address = models.TextField(null=True, blank=True,verbose_name='Current address')
    state = models.CharField(max_length=255,default='ap')

    groups = models.ManyToManyField(
        "auth.Group", related_name="customuser_set", blank=True, help_text="The groups this user belongs to."
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission", related_name="customuser_set", blank=True, help_text="Specific permissions for this user."
    )

    def save(self, *args, **kwargs):
        if not self.username or self.username == 'sdeuser789':
            max_value = CustomUser.objects.filter(username__startswith='sdeuser').aggregate(models.Max('username'))['username__max']
            if max_value is not None:
                increment_value = int(max_value[len('sdeuser') :]) + 1
                self.username = 'sdeuser' + str(increment_value)
            else:
                self.username = 'sdeuser789'
        super().save(*args, **kwargs)
    def __str__(self):
        return self.username
        

class ContactSubmission(models.Model):
    full_name = models.CharField(max_length=30)
    email = models.EmailField()
    message = models.TextField()
    response = models.TextField(default='-----', blank=True)

    def __str__(self):
        return self.full_name

class SoftwareJob(models.Model):
    job_name = models.CharField(max_length=100)
    min_experience = models.PositiveIntegerField(default=0)
    max_experience = models.PositiveIntegerField(default=0)
    openings = models.PositiveIntegerField()
    min_package = models.PositiveIntegerField(default=0)
    max_package = models.PositiveIntegerField(default=0)
    skills = models.TextField()
    education = models.CharField(max_length=255)
    WORK_MODE_CHOICES = [
        ('hybrid', 'Hybrid'),
        ('remote', 'Remote'),
        ('office', 'Office'),
    ]
    work_mode = models.CharField(max_length=10, choices=WORK_MODE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    job_description = models.TextField()

    def save(self, *args, **kwargs):
        self.job_name = self.job_name.title()
        self.skills = self.skills.title()
        self.education = self.education.title()
        self.job_description = self.job_description.capitalize()
        self.clean()  # Call clean method for validation
        super(SoftwareJob, self).save(*args, **kwargs)

    def clean(self):
        if self.min_experience > self.max_experience:
            raise ValidationError("Minimum experience should be less than maximum experience.")
        if self.min_package > self.max_package:
            raise ValidationError("Minimum package should be less than maximum package.")

    def __str__(self):
        return f"{self.job_name}"

class JobSubmission(models.Model):
    EXPERIENCE_CHOICES = [
        (0, '0 Fresher'),
        (1, '1 Year'),
        (2, '2 Years'),
        (3, '3 Years'),
        (4, '4 Years'),
        (5, '5+ Years'),
        # Add more choices as needed
    ]
    RESULT_CHOICES = [
        ('shortlisted', 'Shortlisted'),
        ('not_shortlisted', 'Not Shortlisted'),
    ]
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=None)
    SoftwareJob = models.ForeignKey(SoftwareJob, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    education = models.CharField(max_length=255)
    branch = models.CharField(max_length=255)
    graduation_year = models.PositiveIntegerField()
    experience = models.IntegerField(choices=EXPERIENCE_CHOICES)
    resume = models.FileField(upload_to='resumes/')
    result = models.CharField(max_length=20, choices=RESULT_CHOICES, default='Pending', blank=True)
    user_has_applied = models.BooleanField(default=False)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} applied for {self.SoftwareJob.job_name}"

