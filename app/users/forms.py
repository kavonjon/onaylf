# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import User, Organization

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
        fields = ('email', 'first_name', 'last_name')

# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = User
#         prefix = 'user_profile'
#         fields = ['organization',
#                   'phone',
#                   'alt_phone',
#                   'fax',
#                   'alt_email',
#                   'address',
#                   'city',
#                   'state',
#                   'zip',]
        

# class UserEditForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['email',
#                   'first_name',
#                   'last_name',
#                   'organization',
#                   'phone',
#                   'alt_phone',
#                   'fax',
#                   'alt_email',
#                   'address',
#                   'city',
#                   'state',
#                   'zip',]
        
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Add Bootstrap classes to form fields
#         for field in self.fields.values():
#             field.widget.attrs['class'] = 'form-control'


class UserEditForm(forms.ModelForm):
    ORGANIZATION_OTHER = 'other'
    
    organization_choice = forms.ChoiceField(
        choices=[('', 'Select a program/school...')],
        required=True,
        label="Program/School*"
    )
    other_organization = forms.CharField(
        max_length=255,
        required=False,
        label="Other program/school name*",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'organization_choice',
            'other_organization',
            'phone',
            'alt_phone',
            'fax',
            'alt_email',
            'address',
            'city',
            'state',
            'zip',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set up organization choices
        org_choices = [('', 'Select a program/school...')]
        org_choices.extend([(org.id, org.name) for org in Organization.objects.all()])
        org_choices.append((self.ORGANIZATION_OTHER, 'Other'))
        self.fields['organization_choice'].choices = org_choices
        
        # Set initial value based on user's current organization
        if self.instance.organization:
            org = Organization.objects.filter(name=self.instance.organization).first()
            if org:
                self.fields['organization_choice'].initial = org.id
            else:
                self.fields['organization_choice'].initial = self.ORGANIZATION_OTHER
                self.fields['other_organization'].initial = self.instance.organization

        # Add Bootstrap classes to form fields
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        org_choice = cleaned_data.get('organization_choice')
        other_org = cleaned_data.get('other_organization')

        if org_choice == self.ORGANIZATION_OTHER and not other_org:
            raise forms.ValidationError("Please specify the program/school name.")
        elif not org_choice and not other_org:
            raise forms.ValidationError("Please select a program/school or specify a new one.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        org_choice = self.cleaned_data.get('organization_choice')
        
        if org_choice == self.ORGANIZATION_OTHER:
            user.organization = self.cleaned_data.get('other_organization')
        else:
            org = Organization.objects.filter(id=org_choice).first()
            user.organization = org.name if org else ''

        if commit:
            user.save()
        return user



class UserProfileForm(forms.ModelForm):
    ORGANIZATION_OTHER = 'other'
    
    organization_choice = forms.ChoiceField(
        choices=[('', 'Select a program/school...')],  # Add empty default option
        required=True,  # Make it required
        label="Program/School*"
    )
    other_organization = forms.CharField(
        max_length=255,
        required=False,
        label="Other program/school name*",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'organization_choice',
            'other_organization',
            'phone',
            'alt_phone',
            'fax',
            'alt_email',
            'address',
            'city',
            'state',
            'zip'
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Hide fields if user is not a moderator
        if user and not user.groups.filter(name='moderator').exists():
            self.fields['email'].widget = forms.HiddenInput()
            self.fields['first_name'].widget = forms.HiddenInput()
            self.fields['last_name'].widget = forms.HiddenInput()

        # Set up organization choices, keeping empty option at the top
        org_choices = [('', 'Select a program/school...')]
        org_choices.extend([(org.id, org.name) for org in Organization.objects.all()])
        org_choices.append((self.ORGANIZATION_OTHER, 'Other'))
        self.fields['organization_choice'].choices = org_choices
        
        # Set initial value based on user's current organization
        if self.instance.organization:
            org = Organization.objects.filter(name=self.instance.organization).first()
            if org:
                self.fields['organization_choice'].initial = org.id
            else:
                self.fields['organization_choice'].initial = self.ORGANIZATION_OTHER
                self.fields['other_organization'].initial = self.instance.organization

    def clean(self):
        cleaned_data = super().clean()
        org_choice = cleaned_data.get('organization_choice')
        other_org = cleaned_data.get('other_organization')

        if org_choice == self.ORGANIZATION_OTHER and not other_org:
            raise forms.ValidationError("Please specify the program/school name.")
        elif not org_choice and not other_org:
            raise forms.ValidationError("Please select a program/school or specify a new one.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        org_choice = self.cleaned_data.get('organization_choice')
        
        if org_choice == self.ORGANIZATION_OTHER:
            user.organization = self.cleaned_data.get('other_organization')
        else:
            org = Organization.objects.filter(id=org_choice).first()
            user.organization = org.name if org else ''

        if commit:
            user.save()
        return user