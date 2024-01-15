# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User  # use your custom user model
        fields = ('email', 'first_name', 'last_name', 'organization')  # add additional fields if needed