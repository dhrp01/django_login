import datetime

from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect

class SessionTimeoutMiddleware:
    """Check for inactivity and logout the user after timeout expires"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            now = datetime.datetime.now()
            last_activity = request.session.get('last_activity')

            if last_activity:
                elapsed_time = (now - datetime.datetime.fromisoformat(last_activity)).seconds
                if elapsed_time > getattr(settings, 'SESSION_TIMEOUT', 60*10):
                    logout(request)
                    return redirect('login')
            request.session['last_activity'] = now.isoformat()

        return self.get_response(request)
