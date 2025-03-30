import os
import time
from django.conf import settings

class DemoTimestampMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Define paths relative to BASE_DIR
        self.base_dir = settings.BASE_DIR
        self.timestamp_dir = os.path.join(self.base_dir, 'demo_timestamps')
        self.modified_file = os.path.join(self.timestamp_dir, 'demo_last_modified.timestamp')
        
        # Create timestamp directory if it doesn't exist
        if settings.DEMO_MODE and not os.path.exists(self.timestamp_dir):
            os.makedirs(self.timestamp_dir)

    def __call__(self, request):
        response = self.get_response(request)
        
        # Only track timestamps in demo mode for data-changing requests
        if settings.DEMO_MODE and request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
            with open(self.modified_file, 'w') as f:
                f.write(str(int(time.time())))
        
        return response