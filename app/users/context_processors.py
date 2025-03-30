from django.conf import settings

def user_context(request):
    return {
        'moderator': request.user.groups.filter(name='moderator').exists() if request.user.is_authenticated else False
    }

def demo_mode_context(request):
    """
    Adds demo mode context variable to all templates
    """
    print(f"DEMO_MODE in context processor: {settings.DEMO_MODE}")
    return {
        'DEMO_MODE': settings.DEMO_MODE,
        'DEMO_NOTICE': "This is a demo version with sample data. For the full application, please visit the main site." if settings.DEMO_MODE else None,
    }