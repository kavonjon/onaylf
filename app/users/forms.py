# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import User

# class CustomUserCreationForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = User  # use your custom user model
#         fields = ('email', 'first_name', 'last_name', 'organization', 'phone', 'alt_phone', 'fax', 'alt_email', 'address', 'city', 'state', 'zip')  # add additional fields if needed


# class CustomUserCreationForm(UserCreationForm):
#     # email = forms.EmailField(required=True)
#     # first_name = forms.CharField(required=True)
#     # last_name = forms.CharField(required=True)
#     # organization = forms.CharField(required=True)
#     # phone = forms.CharField(required=False)
#     # alt_phone = forms.CharField(required=True)
#     # fax = forms.CharField(required=True)
#     # alt_email = forms.EmailField(required=True)
#     # address = forms.CharField(required=True)
#     # city = forms.CharField(required=True)
#     # state = forms.CharField(required=True)
#     # zip = forms.CharField(required=True)

#     class Meta:
#         model = User
#         fields = ("email", "first_name", "last_name", "organization", "phone", "alt_phone", "fax", "alt_email", "address", "city", "state", "zip", "password1", "password2")

#     def save(self, commit=True):
#         user = super(CustomUserCreationForm, self).save(commit=False)
#         user.email = self.cleaned_data['email']
#         if commit:
#             user.save()
#         return user

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User  # use your custom user model
        fields = ('email', 'first_name', 'last_name', 'organization')  # add additional fields if needed

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        prefix = 'user_profile'
        fields = ['organization',
                  'phone',
                  'alt_phone',
                  'fax',
                  'alt_email',
                  'address',
                  'city',
                  'state',
                  'zip',]