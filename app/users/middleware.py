from django.shortcuts import redirect
from django.urls import resolve
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class YearlyProfileCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if not request.user.groups.filter(name='moderator').exists():
                current_url = resolve(request.path_info).url_name
                if current_url not in ['user_account_detail', 'user_account_edit', 'logout']:
                    previous_login_year = request.session.get('previous_login')
                    current_year = datetime.now().year
                    
                    
                    if previous_login_year and previous_login_year < current_year:
                        # Store the full URL including query parameters
                        next_url = request.get_full_path()
                        request.session['next_url'] = next_url
                        return redirect('user_account_detail')

        response = self.get_response(request)
        return response