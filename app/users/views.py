from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm
from django.urls import reverse
from django.views import generic
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from .models import Organization, User
from submissions.models import CurrentFair, Submission
from .forms import UserProfileForm, UserEditForm
from datetime import datetime
from django.db import transaction
from django.db.models.functions import Lower
from django.views.decorators.http import require_POST, require_http_methods
import logging
from django.contrib.auth.hashers import make_password

logger = logging.getLogger(__name__)

def is_moderator(user):
    return user.groups.filter(name='moderator').exists()


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'

    def dispatch(self, request, *args, **kwargs):
        # Check if registration is closed
        current_fair = CurrentFair.objects.first()
        if not current_fair or not current_fair.fair.registration_open:
            messages.error(request, f'Registration is currently closed')
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return '/accounts/profile/edit/'

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

@require_POST
@login_required
@user_passes_test(is_moderator)
def confirm_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.confirmed = True
        user.save()
        return JsonResponse({'status': 'success'})
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

@require_http_methods(["DELETE"])
@login_required
@user_passes_test(is_moderator)
def delete_user(request, user_id):
    try:
        # Don't allow deletion of self
        if request.user.id == user_id:
            logger.warning(f"User {request.user.id} attempted to delete their own account")
            return JsonResponse({'error': 'Cannot delete your own account'}, status=400)
            
        user = User.objects.get(id=user_id)
        
        # Check if user has any submissions (this will block deletion)
        submissions = Submission.objects.filter(user=user)
        if submissions.exists():
            logger.warning(f"Cannot delete user {user_id} - has {submissions.count()} submissions")
            return JsonResponse({
                'error': f'Cannot delete user with existing submissions ({submissions.count()} found). Please delete or reassign their submissions first.',
                'blockDelete': True
            }, status=400)
        
        # Log deletion attempt    
        logger.info(f"Attempting to delete user {user.id} ({user.email})")
        
        # Check for related objects that will be cascade deleted
        instructor_count = user.instructor_user.count()
        student_count = user.student_user.count()
        
        # If there are related records and this isn't a confirmed delete, show warning
        if (instructor_count > 0 or student_count > 0) and 'X-Confirm-Delete' not in request.headers:
            warning_parts = []
            if instructor_count > 0:
                warning_parts.append(f"{instructor_count} Instructor{'s' if instructor_count > 1 else ''}")
            if student_count > 0:
                warning_parts.append(f"{student_count} Student{'s' if student_count > 1 else ''}")
                
            return JsonResponse({
                'warning': f"Deleting user will also delete related data ({', '.join(warning_parts)})",
                'blockDelete': False
            }, status=200)
            
        # If we get here, either there are no related records or this is a confirmed delete
        user.delete()
        logger.info(f"Successfully deleted user {user_id}")
        return JsonResponse({'status': 'success'})
        
    except User.DoesNotExist:
        logger.warning(f"Attempted to delete non-existent user {user_id}")
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {str(e)}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)

@user_passes_test(is_moderator)
def user_add(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Generate a random password that the user will need to reset
            temp_password = User.objects.make_random_password()
            user.password = make_password(temp_password)
            user.confirmed = True  # Automatically confirm users added by moderators
            user.save()
            
            messages.success(request, f'User {user.email} has been created successfully.')
            return redirect('user_detail', user_pk=user.id)
    else:
        form = UserEditForm()
    
    return render(request, 'user_add.html', {'form': form})