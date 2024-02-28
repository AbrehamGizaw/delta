# useracc/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('email_verified', 'Email_verified'),
        ('activated', 'Activated'),
    ]

    username = models.CharField(max_length=150, unique=True)
    fullname = models.CharField(max_length=50,)
    phone = models.CharField(max_length=13)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_superuser = models.BooleanField(default=False)
    profile = models.ImageField(upload_to='Profile', blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.username
