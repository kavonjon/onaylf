from django.conf import settings
import os
from django.contrib.auth.models import Group
from django.db.models import Q

def user_context(request):
    return {
        'moderator': request.user.groups.filter(name='moderator').exists() if request.user.is_authenticated else False
    }

def demo_mode_context(request):
    """
    Adds demo mode context variable to all templates
    """
    print(f"DEMO_MODE in context processor: {settings.DEMO_MODE}")
    
    context = {
        'DEMO_MODE': settings.DEMO_MODE,
        'DEMO_NOTICE': "This is a demo version with sample data. For the full application, please visit the main site." if settings.DEMO_MODE else None,
    }
    
    if settings.DEMO_MODE:
        # Import User model here to avoid circular imports
        from users.models import User
        
        # Get moderator group
        mod_group = Group.objects.filter(name='moderator').first()
        
        if mod_group:
            # Get moderators who are not staff/superusers
            moderators = User.objects.filter(
                groups=mod_group,
                is_staff=False,
                is_superuser=False
            ).values_list('email', flat=True)
            
            # Get regular users who are not moderators, staff, or superusers
            regular_users = User.objects.filter(
                ~Q(groups=mod_group),
                is_staff=False,
                is_superuser=False
            ).values_list('email', flat=True)
            
            context.update({
                'DEMO_MODERATORS': list(moderators),
                'DEMO_USERS': list(regular_users),
                'DEMO_MODERATOR_PASSWORD': os.getenv('MODERATORS_PASSWORD', ''),
                'DEMO_USER_PASSWORD': os.getenv('BASIC_USER_PASSWORD', ''),
            })
    
    return context