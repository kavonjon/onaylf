from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from submissions.models import STATE_CHOICES
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from datetime import datetime
from django.db.models.functions import Lower

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    organization = models.CharField(max_length=500, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    alt_phone = models.CharField(max_length=20, blank=True, null=True)
    fax = models.CharField(max_length=20, blank=True, null=True)
    alt_email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=2, choices=STATE_CHOICES, blank=True, null=True)
    zip = models.CharField(max_length=10, blank=True, null=True)
    confirmed = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    


    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # In Django, the USERNAME_FIELD is required by default.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Store the original values when the instance is loaded
        self._loaded_values = dict(organization=self.organization)

    class Meta:
        ordering = (Lower('last_name'), Lower('first_name'))


# class FairUser(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     organization = models.CharField(max_length=500)

class Organization(models.Model):
    name = models.CharField(max_length=500, unique=True)
    def __str__(self):
        return self.name

@receiver(user_logged_in)
def store_last_login(sender, user, request, **kwargs):
    """Store the previous last_login in the session before it gets updated"""
    if user.last_login:
        request.session['previous_login'] = user.last_login.year
    else:
        request.session['previous_login'] = None
