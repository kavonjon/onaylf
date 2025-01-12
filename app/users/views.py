from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm
from django.urls import reverse
from django.views import generic
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from .models import Organization, User
from submissions.models import CurrentFair
from .forms import UserProfileForm, UserEditForm
from datetime import datetime
from django.db import transaction
from django.db.models.functions import Lower
from .utils import generate_registration_code

def is_moderator(user):
    return user.groups.filter(name='moderator').exists()


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    # success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return '/accounts/profile/edit/'

    def form_valid(self, form):
        # Get the registration code from POST data
        submitted_code = self.request.POST.get('registration_code')
        expected_code = generate_registration_code()

        # Check if the submitted code matches
        if submitted_code != expected_code:
            form.add_error(None, "Invalid registration code")
            return self.form_invalid(form)

        return super().form_valid(form)

@login_required
def user_account_detail(request):
    currentUser = User.objects.get(pk=request.user.pk)
    current_year = datetime.now().year
    
    show_update_notice = False
    if not request.user.groups.filter(name='moderator').exists():
        previous_login_year = request.session.get('previous_login')
        if previous_login_year and previous_login_year < current_year:
            show_update_notice = True
    
    # Get and print the next URL for debugging
    next_url = request.session.get('next_url')
    
    # Clear both the next_url and previous_login from session
    if next_url:
        del request.session['next_url']
    # Update previous_login to current year to prevent further redirects
    request.session['previous_login'] = current_year
    
    context = {
        'currentUser': currentUser,
        'currentFair': CurrentFair.objects.first().name if CurrentFair.objects.first() else None,
        'show_update_notice': show_update_notice,
        'next_url': next_url,
    }
    return render(request, 'registration/user_account_detail.html', context)

@login_required
def user_account_edit(request):

    currentFair = CurrentFair.objects.first()

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=request.user, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_account_detail')
    else:
        form = UserProfileForm(instance=request.user, user=request.user)

    template = 'registration/user_account_edit.html'
    context = {
        'currentFair': currentFair.name,
        'form': form,
        'error_message': form.errors.get('__all__', '') if request.method == 'POST' else None

    }
    return render(request, template, context)

@login_required
@user_passes_test(is_moderator)
def user_edit(request, user_id):
    """
    View for moderators/admins to edit other users' profiles
    """
    user_to_edit = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=user_to_edit)
        if form.is_valid():
            form.save()
            messages.success(request, f'Profile updated successfully for {user_to_edit.first_name} {user_to_edit.last_name} ({user_to_edit.email})')
            return redirect('user_list')  # Or wherever you want to redirect after success
    else:
        form = UserEditForm(instance=user_to_edit)
    
    return render(request, 'user_edit.html', {
        'form': form,
        'edited_user': user_to_edit
    })

@user_passes_test(is_moderator)
def organization_list(request):
    organizations = Organization.objects.all().order_by(Lower('name'))
    return render(request, 'organization_list.html', {'organizations': organizations})

@user_passes_test(is_moderator)
def organization_add(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=400)
    
    name = request.POST.get('name', '').strip()
    if not name:
        return JsonResponse({'error': 'Name is required'}, status=400)
        
    if Organization.objects.filter(name=name).exists():
        return JsonResponse({'error': 'Organization with this name already exists'}, status=400)
        
    org = Organization.objects.create(name=name)
    return JsonResponse({'id': org.id, 'name': org.name})

@user_passes_test(is_moderator)
def organization_edit(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=400)
        
    org = get_object_or_404(Organization, pk=pk)
    new_name = request.POST.get('name', '').strip()
    
    if not new_name:
        return JsonResponse({'error': 'Name is required'}, status=400)
        
    if Organization.objects.filter(name=new_name).exclude(pk=pk).exists():
        return JsonResponse({'error': 'Organization with this name already exists'}, status=400)
    
    old_name = org.name
    with transaction.atomic():
        # Update organization name
        org.name = new_name
        org.save()
        
        # Update all users who had the old organization name
        User.objects.filter(organization=old_name).update(organization=new_name)
        
    return JsonResponse({'id': org.id, 'name': new_name})

@user_passes_test(is_moderator)
def organization_delete(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=400)
        
    org = get_object_or_404(Organization, pk=pk)
    affected_users = User.objects.filter(organization=org.name).count()
    
    # Check if this is just a preliminary check
    if request.POST.get('check_only') == 'true':
        # Return count of affected users and list of other organizations
        other_orgs = Organization.objects.exclude(pk=pk).order_by('name')
        return JsonResponse({
            'affected_users': affected_users,
            'organizations': list(other_orgs.values('id', 'name'))
        })
    
    # If there are affected users, we need a new organization
    if affected_users > 0 and 'new_organization' not in request.POST:
        return JsonResponse({'error': 'New organization required'}, status=400)
    
    with transaction.atomic():
        new_org_data = None
        if affected_users > 0:
            new_org = request.POST.get('new_organization')
            other_org_name = request.POST.get('other_organization', '')
            add_as_org = request.POST.get('add_as_org') == 'true'
            
            if new_org == 'other':
                if not other_org_name:
                    return JsonResponse({'error': 'New organization name is required'}, status=400)
                new_org_name = other_org_name
                if add_as_org:
                    new_org_obj = Organization.objects.create(name=other_org_name)
                    new_org_data = {'id': new_org_obj.id, 'name': new_org_obj.name}
            else:
                new_org_obj = get_object_or_404(Organization, pk=new_org)
                new_org_name = new_org_obj.name
            
            # Update users individually to trigger signals
            for user in User.objects.filter(organization=org.name):
                user.organization = new_org_name
                user.save()
        
        org.delete()
        
        response_data = {'success': True}
        if new_org_data:
            response_data['new_organization'] = new_org_data
        return JsonResponse(response_data)