from django.apps import AppConfig
from django.conf import settings

class SubmissionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'submissions'

    def ready(self):
        """Initialize the application and start the scheduler"""

        
        # Only import and start scheduler if in DEMO_MODE
        if settings.DEMO_MODE:
            from submissions.scheduler import start_scheduler
            start_scheduler()

        import submissions.signals